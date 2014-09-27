from django.conf.urls import patterns, include, url
from django.contrib import admin
from os import path

admin.autodiscover()
BASEDIR = path.dirname(path.abspath(__file__))

urlpatterns = patterns('',
    # URLS for OpenId authentication
    url(r'^$', 'linking_service.views.home', name='home'),
    url(r'^api/get_userid$', 'linking_service.api.get_userid', name='get_userid'),
    url(r'^login/', 'linking_service.views.login', name='login'),

    url(r'^oidc/', include('oidc_django.urls', namespace='oidc_django')),
    url(r'^shib/', include('shib_django.urls', namespace='shib_django')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': path.join(BASEDIR, "static")})
)
