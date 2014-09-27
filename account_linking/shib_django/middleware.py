from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject

from django.shortcuts import render
from mako.lookup import TemplateLookup
from djangomako.shortcuts import render_to_response
from django.http import HttpResponse
from urlparse import parse_qs
from backends import ShibbolethUserBackend

from shib_django.conf import SHIBBOLETH_ATTRIBUTE_MAP

import urllib
import threading

class ShibbolethMiddleware(RemoteUserMiddleware):
    """
    Middleware for utilizing OpenId authentication.

    If request.user is not authenticated, then this middleware attempts to
    authenticate the username with OpenId connect.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.
    """

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the OpenIdUserMiddleware class.")

        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
	    return

        try:
            username = request.META[self.header]
            # Make sure we have all required Shiboleth elements before proceeding.
            shib_meta, error = self.parse_attributes(request)
            # Add parsed attributes to the session.
            request.session['shib'] = shib_meta
            if error:
                raise ShibbolethValidationError("All required Shibboleth elements"
                                                " not found.  %s" % shib_meta)
        except Exception, e:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated():
                try:
                    stored_backend = load_backend(request.session.get(
                        auth.BACKEND_SESSION_KEY, ''))
                    if isinstance(stored_backend, ShibbolethUserBackend):
                        auth.logout(request)
                except ImproperlyConfigured as e:
                    # backend failed to load
                    auth.logout(request)
        else:
            # We are seeing this user for the first time in this session, attempt
            # to authenticate the user.
            user = auth.authenticate(shib_meta=shib_meta)
            if user:
                # User is valid.  Set request.user and persist user in the session
                # by logging the user in.
                request.user = user
                auth.login(request, user)

    def clean_username(self, username, request):
        """
        Allows the backend to clean the username, if the backend defines a
        clean_username method.
        """
        backend_str = request.session[auth.BACKEND_SESSION_KEY]
        backend = auth.load_backend(backend_str)
        try:
            username = backend.clean_username(username)
        except AttributeError:  # Backend has no clean_username method.
            pass
        return username

    def parse_attributes(self, request):
        """
        Parse the incoming Shibboleth attributes.
        From: https://github.com/russell/django-shibboleth/blob/master/django_shibboleth/utils.py
        Pull the mapped attributes from the apache headers.
        """
        shib_attrs = {}
        error = False
        meta = request.META
        for header, attr in SHIBBOLETH_ATTRIBUTE_MAP.items():
            required, name = attr
            value = meta.get(header, None)
            shib_attrs[name] = value
            if not value or value == '':
                if required:
                    error = True
        return shib_attrs, error

class ShibbolethValidationError(Exception):
    pass
