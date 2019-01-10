# -*- coding: utf-8 -*-

from django.conf.urls import patterns,url,include

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^history/$','history'),
    url(r'^api/', include('home_application.api.urls')),
)
