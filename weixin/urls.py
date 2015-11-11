# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

__author__ = 'JiaPan'

urlpatterns = patterns('',
                       url(r'^$', 'weixin.views.handleRequest'),
                       url(r'^contact/$', 'weixin.views.contact'),
                       url(r'^send_dynamic/(?P<openid>.*?)/(?P<phone>\d+)/$', 'weixin.views.send_dynamic'),
                       url(r'^register/success/$', 'weixin.views.register_success', name='register_success'),
                       url(r'^register/already/$', 'weixin.views.register_already', name='register_already'),
                       url(r'^register/(?P<openid>.*?)/$', 'weixin.views.register'),
)
