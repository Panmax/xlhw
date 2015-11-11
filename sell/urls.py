# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

__author__ = 'JiaPan'

urlpatterns = patterns('',
                       url(r'^$', 'sell.views.index'),
)