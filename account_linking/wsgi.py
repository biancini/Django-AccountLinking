import os
import sys

path = "/var/www/"
if path not in sys.path:
    sys.path.append(path)

path = "/var/www/account_linking"
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "account_linking.settings")

from oidc_django import oidc, conf
from django.core.handlers.wsgi import WSGIHandler
_application = WSGIHandler()

global OIDC_CLIENTS
OIDC_CLIENTS = oidc.OIDCClients(conf)

def application(environ, start_response):
    global OIDC_CLIENTS
    environ['OIDC_CLIENTS'] = OIDC_CLIENTS

    return _application(environ, start_response)
