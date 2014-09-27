from account_linking.oidc_django.middleware import OpenIdMiddleware
from account_linking.shib_django.middleware import ShibbolethMiddleware
from account_linking.models import LastLogin
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

class AccountLinkingMiddleware(object):
    """
    ddleware for utilizing Account Linking authentication.
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

        if "login_with" in request.session.keys():
            if request.session["login_with"] == "Shibboleth":
                middleware = ShibbolethMiddleware()
            elif request.session["login_with"] == "OpenID":
                middleware = OpenIdMiddleware()
            else:
                middleware = None

            if middleware:
                middleware.process_request(request)

                if request.user.is_authenticated():
                    try:
                        login = LastLogin.objects.get(username=request.user.username)
                        request.session["login_date"] = str(login.login_date)
                        request.session["login_method"] = login.login_method
                    except ObjectDoesNotExist:
                        login = LastLogin(username=request.user.username, 
                                          login_date=datetime.now(),
                                          login_method=request.session["login_with"])
                        request.session["login_date"] = "NEVER"
                        request.session["login_method"] = "NONE"

                    login.login_date=datetime.now()
                    login.login_method=request.session["login_with"]
                    login.save()

                    print "Authenticated user with %s" % request.session["login_with"]
