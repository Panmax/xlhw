# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

__author__ = 'JiaPan'

urlpatterns = patterns('',
                       url(r'^$', 'meizu.views.all_phone'),

                       url(r'^all/phone/$', 'meizu.views.all_phone', name='meizu_allphone'),
                       url(r'^guoao/phone/$', 'meizu.views.guoao_phone', name='meizu_guoaophone'),
                       url(r'^dadian/phone/$', 'meizu.views.dadian_phone', name='meizu_dadianphone'),
                       url(r'^hongwei/phone/$', 'meizu.views.hongwei_phone', name='meizu_hongweiphone'),

                       url(r'^all/peijian/$', 'meizu.views.all_peijian', name='meizu_allpeijian'),
                       url(r'^guoao/peijian/$', 'meizu.views.guoao_peijian', name='meizu_guoaopeijian'),
                       url(r'^dadian/peijian/$', 'meizu.views.dadian_peijian', name='meizu_dadianpeijian'),
                       url(r'^hongwei/peijian/$', 'meizu.views.hongwei_peijian', name='meizu_hongweipeijian'),

                       url(r'^add/$', 'meizu.views.add_goods', name="meizu_addgoods"),
                       url(r'^login/$', 'meizu.views.mylogin', name='meizu_mylogin'),
                       url(r'^login/fail$', 'meizu.views.login_fail', name='meizu_login_fail'),
                       url(r'^logout/$', 'meizu.views.mylogout', name="meizu_logout"),
                       url(r'^add/success/$', 'meizu.views.add_success', name="meizu_addsuccess"),

                       url(r'^api/remain/$', 'meizu.views.api_remain', name="meizu_api_remain"),
                       url(r'^api/diaoku/$', 'meizu.views.api_diaoku', name="meizu_api_diaoku"),
                       url(r'^api/update/$', 'meizu.views.api_update', name="meizu_api_update"),
                       url(r'^api/delete_goods_record/$', 'meizu.views.api_delete_goods_record',
                           name="meizu_api_delete_goods_record"),
                       url(r'^api/delete_goods/$', 'meizu.views.delete_goods',
                           name="meizu_api_delete_goods"),
                       url(r'^api/setcolor/$', 'meizu.views.api_setcolor', name="meizu_api_setcolor"),
                       url(r'^api/showcolor/$', 'meizu.views.api_showcolor', name="meizu_api_showcolor"),


                       url(r'^outin/$', 'meizu.views.out_in', name="meizu_out_in"),
                       url(r'^checkoutin/$', 'meizu.views.check_out_in', name="meizu_check_out_in"),
                       url(r'^transfer/$', 'meizu.views.transfer', name="meizu_transfer"),
                       url(r'^changeprice/$', 'meizu.views.change_price', name="meizu_change_price"),
                       url(r'^return_record/$', 'meizu.views.return_record', name="meizu_return_record"),

                       url(r'^checkbackup/$', 'meizu.views.check_backup', name="meizu_check_backup"),
                       url(r'^backup/$', 'meizu.views.mybackup', name="meizu_backup"),

                       url(r'^delete_goods/$', 'meizu.views.delete_goods', name="meizu_delete_goods"),

                       # url(r'^modal/diaoku/$', 'meizu.views.modal_diaoku', name="modal_diaoku"),
                       url(r'^chart/sell_ranking/$', 'meizu.views.sell_ranking_chart', name="meizu_sell_ranking_chart"),

                       url(r'^single_goods_detail/$', 'meizu.views.single_goods_detail', name="meizu_single_goods_detail"),

)