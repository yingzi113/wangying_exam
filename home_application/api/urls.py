# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.api.views',
    (r'^test/$', 'test'),
    (r'^search_business/$', 'search_business'),
    (r'^get_set_list/$', 'get_set_list'),
    (r'^get_host/$', 'get_host'),
    (r'^get_job_detail/$','get_job_detail'),
    (r'^execute_job/$','execute_job'),
    (r'^get_records/$','get_records'),
)