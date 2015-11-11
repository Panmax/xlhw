# -*- coding: utf-8 -*-

import urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from random import choice
from models import User, PhonePaste, PhonePasteTransfer, PhonePasteRecoder, StaffSignRecord
import string
from django.core.exceptions import ObjectDoesNotExist

#python3中为string.ascii_letters,而python2下则可以使用string.letters和string.ascii_letters

def get_password(length=4, chars=string.digits):#chars=string.ascii_letters + string.digits
    return ''.join([choice(chars) for i in range(length)])

def send_dynamic_sms(number):
    random_num = get_password()
    content = '您的随机验证码为%s。【新乐微信平台】' % random_num
    url = "http://www.smsbao.com/sms?u=xlhw&p=cec31f43dfdc269185dd3d12551e9721&m=%s&c=%s"

    # content = '您的随机密码为%s。【邯郸微信平台】' % random_num
    # url = "http://www.smsbao.com/sms?u=jiapan&p=e10adc3949ba59abbe56e057f20f883e&m=%s&c=%s"

    req = urllib2.Request(url % (number, content))
    # print req
    # print content

    res_data = urllib2.urlopen(req)
    res = res_data.read()
    return res, random_num

def check_regist(openid):
    try:
        u = User.objects.get(openid=openid)
    except:
        return False
    else:
        return True

def get_or_create_user_phone_paste(openid):
    u = User.objects.get(openid=openid)
    try:
        p = PhonePaste.objects.get(user=u)
    except ObjectDoesNotExist:
        p = PhonePaste(user=u, remain=0)
        p.save()

    return p

def get_week_day(weekday):
    if weekday == 0:
        return u'星期一'
    if weekday == 1:
        return u'星期二'
    if weekday == 2:
        return u'星期三'
    if weekday == 3:
        return u'星期四'
    if weekday == 4:
        return u'星期五'
    if weekday == 5:
        return u'星期六'
    if weekday == 6:
        return u'星期日'




if __name__ == '__main__':
    print send_dynamic_sms('13313316369')