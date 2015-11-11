# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

__author__ = 'JiaPan'

urlpatterns = patterns('',
                       url(r'^$', 'kucun.views.all_phone'),

                       url(r'^all/phone/$', 'kucun.views.all_phone', name='allphone'),
                       url(r'^guoao/phone/$', 'kucun.views.guoao_phone', name='guoaophone'),
                       url(r'^dadian/phone/$', 'kucun.views.dadian_phone', name='dadianphone'),
                       url(r'^hongwei/phone/$', 'kucun.views.hongwei_phone', name='hongweiphone'),

                       url(r'^all/peijian/$', 'kucun.views.all_peijian', name='allpeijian'),
                       url(r'^guoao/peijian/$', 'kucun.views.guoao_peijian', name='guoaopeijian'),
                       url(r'^dadian/peijian/$', 'kucun.views.dadian_peijian', name='dadianpeijian'),
                       url(r'^hongwei/peijian/$', 'kucun.views.hongwei_peijian', name='hongweipeijian'),

                       url(r'^add/$', 'kucun.views.add_goods', name="addgoods"),
                       url(r'^login/$', 'kucun.views.mylogin', name='mylogin'),
                       url(r'^login/fail$', 'kucun.views.login_fail', name='login_fail'),
                       url(r'^logout/$', 'kucun.views.mylogout', name="logout"),
                       url(r'^add/success/$', 'kucun.views.add_success', name="addsuccess"),

                       url(r'^api/remain/$', 'kucun.views.api_remain', name="api_remain"),
                       url(r'^api/diaoku/$', 'kucun.views.api_diaoku', name="api_diaoku"),
                       url(r'^api/update/$', 'kucun.views.api_update', name="api_update"),
                       url(r'^api/delete_goods_record/$', 'kucun.views.api_delete_goods_record',
                           name="api_delete_goods_record"),
                       url(r'^api/delete_goods/$', 'kucun.views.delete_goods',
                           name="api_delete_goods"),
                       url(r'^api/setcolor/$', 'kucun.views.api_setcolor', name="api_setcolor"),
                       url(r'^api/showcolor/$', 'kucun.views.api_showcolor', name="api_showcolor"),


                       url(r'^outin/$', 'kucun.views.out_in', name="out_in"),
                       url(r'^checkoutin/$', 'kucun.views.check_out_in', name="check_out_in"),
                       url(r'^transfer/$', 'kucun.views.transfer', name="transfer"),
                       url(r'^changeprice/$', 'kucun.views.change_price', name="change_price"),
                       url(r'^return_record/$', 'kucun.views.return_record', name="return_record"),

                       url(r'^checkbackup/$', 'kucun.views.check_backup', name="check_backup"),
                       url(r'^backup/$', 'kucun.views.mybackup', name="backup"),

                       url(r'^delete_goods/$', 'kucun.views.delete_goods', name="delete_goods"),

                       # url(r'^modal/diaoku/$', 'kucun.views.modal_diaoku', name="modal_diaoku"),
                       url(r'^chart/sell_ranking/$', 'kucun.views.sell_ranking_chart', name="sell_ranking_chart"),

                       url(r'^single_goods_detail/$', 'kucun.views.single_goods_detail', name="single_goods_detail"),

)