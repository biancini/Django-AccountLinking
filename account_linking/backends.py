from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.backends import ModelBackend
from account_linking.oidc_django.backends import OpenIdUserBackend
from account_linking.shib_django.backends import ShibbolethUserBackend
from urllib2 import urlopen, URLError
import json

class AccountLinkingUserBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``AccountLinkingUserMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """

    # Create a User object if not already in the database?
    create_unknown_user = True

    def authenticate(self, shib_meta=None, userinfo=None):
        """
        To authenticate engage the OpenId Connect login procedure.
        The username returned by this process is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if shib_meta:
            backend = ShibbolethUserBackend()
            backend.create_unknown_user = False
            user = backend.authenticate(shib_meta=shib_meta)
        elif userinfo:
            backend = OpenIdUserBackend()
            backend.create_unknown_user = False
            user = backend.authenticate(userinfo=userinfo)
        else:
            backend = None
            user = None

        if not backend or not user: return
        user_meta = self.get_userid_from_account_linking_service(user.username)
        username = self.clean_username(user_meta['id'])
        UserModel = get_user_model()

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if self.create_unknown_user:
            user, created = UserModel.objects.get_or_create(**{
                UserModel.USERNAME_FIELD: username,
            })
            if created:
                user = backend.configure_user(user, shib_meta or userinfo)
                user = self.configure_user(user, user_meta)
        else:
            try:
                user = UserModel.objects.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                pass
        return user

    def clean_username(self, username):
        """
        Performs any cleaning on the "username" prior to using it to get or
        create the user object.  Returns the cleaned username.

        By default, returns the username unchanged.
        """
        return username

    def configure_user(self, user, user_meta):
        """
        Configures a user after creation and returns the updated user.

        By default, returns the user unmodified.
        """
        user.__setattr__('first_name', user_meta['name'])
        user.__setattr__('last_name', user_meta['surname'])
        user.__setattr__('email', user_meta['mail'])
        user.save()
        return user

    def get_userid_from_account_linking_service(self, username):
        url = "https://account-linking.mib.garr.it/ls/api/get_userid?authid=%s" % username
        try:
            page = urlopen(url)
        except URLError, e:
            print "Error while opening account linking service page: %s" % e
            return None
        else:
	    return json.loads(page.read())
