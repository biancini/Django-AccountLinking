from django.conf.urls import patterns, url
from os import path

BASEDIR = path.dirname(path.abspath(__file__))

urlpatterns = patterns('',
    # URLS for OpenId authentication
    url(r'^openid$', 'oidc_django.views.openid', name='openid'),
    url(r'^rp$', 'oidc_django.views.rp', name='rp'),
    url(r'^authz_cb$', 'oidc_django.views.authz_cb', name='authz_cb'),
    url(r'^google$', 'oidc_django.views.google', name='google'),
    url(r'^logout$', 'oidc_django.views.logout', name='logout'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': path.join(BASEDIR, "static")})
)
