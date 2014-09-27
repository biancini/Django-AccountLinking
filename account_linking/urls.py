from django.conf.urls import patterns, include, url
from django.contrib import admin
from os import path

admin.autodiscover()
BASEDIR = path.dirname(path.abspath(__file__))

urlpatterns = patterns('',
    # URLS for OpenId authentication
    #url(r'^openid$', 'account_linking.oidc_django.views.openid', name='openid'),
    #url(r'^rp$', 'account_linking.oidc_django.views.rp', name='rp'),
    #url(r'^authz_cb$', 'account_linking.oidc_django.views.authz_cb', name='authz_cb'),
    #url(r'^logout$', 'account_linking.oidc_django.views.logout', name='logout'),
    url(r'^$', 'account_linking.views.home', name='home'),
    url(r'^login/', 'account_linking.views.login', name='login'),

    url(r'^oidc/', include('oidc_django.urls', namespace='oidc_django')),
    url(r'^shib/', include('shib_django.urls', namespace='shib_django')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': path.join(BASEDIR, "static")})
)
