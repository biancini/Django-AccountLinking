from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # URLS for OpenId authentication
    url(r'^shib$', 'shib_django.views.shib', name='shib'),
    url(r'^login$', 'shib_django.views.login', name='login'),
    url(r'^logout$', 'shib_django.views.login', name='logout'),
)
