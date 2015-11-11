# -*- coding: utf-8 -*-
from django.db.models import Q

from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.utils.encoding import smart_str
from wechat_sdk import WechatBasic
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)
from models import Text, News, SendDynamicRecord, User, PhonePaste, PhonePasteRecoder, PhonePasteTransfer, PhonePasteRechargeRecord, StaffSignRecord
from forms import ContactForm, RegistForm
from datetime import date
from tools import send_dynamic_sms, check_regist, get_or_create_user_phone_paste,get_week_day

from django.core.exceptions import ObjectDoesNotExist
import datetime

token = 'XLHW'
wechat = WechatBasic(token=token)


def hello(request):
    return HttpResponse('hello')


def handleRequest(request):
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr", None)
    if request.method == 'GET':
        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            response = HttpResponse(echoStr, content_type="text/plain")
            return response
        else:
            return HttpResponse('error')
    elif request.method == 'POST':
        response = HttpResponse(parserMsg(request), content_type="application/xml")
        return response
    else:
        return None


def parserMsg(request):
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        wechat.parse_data(smart_str(request.body))
        message = wechat.get_message()
        openid = message.source
        response = None
        if isinstance(message, TextMessage):
            content = message.content

            text_auto_reply = Text.objects.filter(commander__commander=content.lower())
            news_auto_reply = News.objects.filter(commander__commander=content).order_by('-priority')[:5]
            if text_auto_reply:
                response = wechat.response_text(content=text_auto_reply[0].content)
            elif news_auto_reply:
                news = []
                for n in news_auto_reply:
                    new = {'title': n.title, 'description': n.description, 'picurl': n.picurl, 'url': n.contenturl}
                    news.append(new)
                    response = wechat.response_news(news)
            else:
                if content == u'注册':
                    if check_regist(openid):
                        response = wechat.response_text(content=u'您已完成注册，谢谢您的支持。')
                    else:
                        url = 'http://xlhw.sinaapp.com/weixin/register/' + openid
                        new = {'title': '注册红卫通讯会员', 'description': '点我开始注册',
                               'picurl': 'http://xlhw-weixin.stor.sinaapp.com/pic/1427089672_853466.png', 'url': url}
                        news = []
                        news.append(new)
                        response = wechat.response_news(news)
                elif content == u'openid':
                    response = wechat.response_text(content=openid)
                elif content == u'贴膜':
                    response = wechat.response_text(content=check_phone_paste(openid))
                elif content == u'我要贴膜':
                    response = wechat.response_text(content=phone_paste_consume(openid))
                elif content[:4] == u'贴膜赠送':
                    phonenumber = content[4:]
                    response = wechat.response_text(content=transfer_phone_paste(openid, phonenumber))
                elif content[:2] == u'充值':
                    phonenumber = content[4:]
                elif content[:4] == u'购机赠膜':
                    phonenumber = content[4:]
                    response = wechat.response_text(content=buy_phone_give_paste(openid, phonenumber))
                elif content == u'打卡':
                    response = wechat.response_text(content=sign_in(openid))
                else:
                    response = wechat.response_text(content=content)
        elif isinstance(message, VoiceMessage):
            response = wechat.response_text(content=u'语音信息')
        elif isinstance(message, ImageMessage):
            response = wechat.response_text(content=u'图片信息')
        elif isinstance(message, VideoMessage):
            response = wechat.response_text(content=u'视频信息')
        elif isinstance(message, LinkMessage):
            response = wechat.response_text(content=u'链接信息')
        elif isinstance(message, LocationMessage):
            response = wechat.response_text(content=u'地理位置信息')
        elif isinstance(message, EventMessage):  # 事件信息
            if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                if message.key and message.ticket:  # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
                    response = wechat.response_text(content=u'欢迎关注新乐市红卫通讯点，敬请期待我们马上开始的微信活动。')
                else:
                    response = wechat.response_text(content=u'欢迎关注新乐市红卫通讯点，敬请期待我们马上开始的微信活动。')
            elif message.type == 'unsubscribe':
                response = wechat.response_text(content=u'取消关注事件')
            elif message.type == 'scan':
                response = wechat.response_text(content=u'用户已关注时的二维码扫描事件')
            elif message.type == 'location':
                response = wechat.response_text(content=u'上报地理位置事件')
            elif message.type == 'click':
                response = wechat.response_text(content=u'自定义菜单点击事件')
            elif message.type == 'view':
                response = wechat.response_text(content=u'自定义菜单跳转链接事件')

        # 现在直接将 response 变量内容直接作为 HTTP Response 响应微信服务器即可，此处为了演示返回内容，直接将响应进行输出
        return response


def contact(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = ContactForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/')  # Redirect after POST
    else:
        form = ContactForm()  # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })


def register(request, openid):
    if len(openid) == 0:
        return HttpResponse('error')
    if request.method == 'POST':
        form = RegistForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phonenumber = form.cleaned_data['phonenumber']
            code = form.cleaned_data['verification_code']
            try:
                record = SendDynamicRecord.objects.get(is_valid=True, phonenumber=phonenumber, password=code, openid=openid)
            except ObjectDoesNotExist:
                form = RegistForm(initial={'name': name, 'phonenumber': phonenumber})
                return render_to_response('register.html', {'form': form, 'code_error': True})
            else:
                record.is_valid = False
                record.save()
                u = User(openid=openid, name=name, phonenumber=phonenumber)
                u.save()
                return HttpResponseRedirect(reverse('register_success'))
    else:
        try:
            u = User.objects.get(openid=openid)
        except ObjectDoesNotExist:
            form = RegistForm()
            return render_to_response('register.html', {'form': form})
        else:
            return HttpResponseRedirect(reverse('register_already'))

def register_success(request):
    return render_to_response('regist_success.html')

def register_already(request):
    return render_to_response('regist_already.html')


def send_dynamic(request, openid, phone):
    today = date.today()
    record = SendDynamicRecord.objects.filter(Q(send_date__startswith=today),
                                              Q(openid=openid) | Q(phonenumber=phone)).count()
    if record <= 100:
        status, password = send_dynamic_sms(phone)
        if status == '0':
            SendDynamicRecord(openid=openid, phonenumber=phone, password=password).save()
            return HttpResponse('success')
    return HttpResponse('false')


def check_phone_paste(openid):
    if not check_regist(openid):
        return u'请先完成注册后再使用本功能。回复【注册】试试吧。'

    p = get_or_create_user_phone_paste(openid)

    return u'您的贴膜可用次数为%s次。 您可回复【我要贴膜】进行消费。 或回复【贴膜赠送】，赠送朋友1次贴膜机会。（现贴膜半价活动进行中，50元10次，详询店内工作人员）' % (p.remain,)

def phone_paste_consume(openid):
    if not check_regist(openid):
        return u'请先完成注册后再使用本功能。回复【注册】试试吧。'

    u = User.objects.get(openid=openid)
    p = get_or_create_user_phone_paste(openid)

    if p.remain <= 0:
        return u'【贴膜】消费失败，您没有可用的贴膜次数。'

    p.remain -= 1
    p.save()

    r=PhonePasteRecoder(user=u, amount=-1)
    r.save()

    date = r.date

    return u'【贴膜】消费成功，消费日期为【%s】，请将本条消息展示于店内工作人员，并且为您提供贴膜服务。您的剩余贴膜次数为【%s】次。（请在3日内使用，过期无效）' % ( date.strftime('%Y-%m-%d %H:%M:%S'), p.remain,)

def recharge(openid, phonenumber):
    superuser_list = ['13313316369', '13143014906', '13180063345', '13143014889']

    superuser = User.objects.get(openid=openid)
    superuser_phone = superuser.phonenumber
    if superuser_phone in superuser_list:
        try:
            u = User.objects.get(phonenumber=phonenumber)
        except ObjectDoesNotExist:
            return u'充值失败，请检查充值号码是否正确，并且已在平台进行注册。'
        else:
            p = get_or_create_user_phone_paste(u.openid)
            p.remain += 10
            p.save()
            PhonePasteRechargeRecord(user=u, updater=superuser, amount=10).save()
            return u'充值成功！\n为【%s】会员充值10次贴膜服务。\n该会员当前贴膜剩余次数为【%s】次。' % (u.name, p.remain)
    else:
        return u'呵呵'

def transfer_phone_paste(openid, phonenumber):
    if not check_regist(openid):
        return u'请先完成注册后再使用本功能。回复【注册】试试吧。'
    from_user = User.objects.get(openid=openid)
    if len(phonenumber) == 0:
        return u'您正在使用贴膜赠送功能，请回复【贴膜赠送+对方手机号】进行贴膜赠送,中间没有空格,每次赠送1次贴膜服务给您的好友。例如：贴膜赠送%s' % (from_user.phonenumber, )
    try:
        to_user = User.objects.get(phonenumber=phonenumber)
    except ObjectDoesNotExist:
        return u'赠送失败，请检查被赠送号码是否正确，并且已在平台进行注册。'
    else:
        if from_user == to_user:
            return u'赠送失败，不能自己赠送给自己。'
        from_user_paste = get_or_create_user_phone_paste(openid)
        to_user_paste = get_or_create_user_phone_paste(to_user.openid)
        from_user_paste.remain-=1
        from_user_paste.save()
        to_user_paste.remain+=1
        to_user_paste.save()
        PhonePasteTransfer(from_user=from_user, to_user=to_user, amount=1).save()
        return u'成功赠送给【%s】1次贴膜服务，您当前剩余贴膜次数为【%s】' % (to_user.name, from_user_paste.remain)


def buy_phone_give_paste(openid, phonenumber):
    superuser_list = ['13313316369', '13143014906', '13180063345', '13143014889']

    superuser = User.objects.get(openid=openid)
    superuser_phone = superuser.phonenumber
    if superuser_phone in superuser_list:
        try:
            u = User.objects.get(phonenumber=phonenumber)
        except ObjectDoesNotExist:
            return u'充值失败，请检查充值号码是否正确，并且已在平台进行注册。'
        else:
            p = get_or_create_user_phone_paste(u.openid)
            p.remain += 3
            p.save()
            PhonePasteRechargeRecord(user=u, updater=superuser, amount=3).save()
            return u'充值成功！\n为【%s】会员充值3次贴膜服务。\n该会员当前贴膜剩余次数为【%s】次。' % (u.name, p.remain)
    else:
        return u'呵呵'

def sign_in(openid):
    if not check_regist(openid):
        return u'请先完成注册后再使用本功能。回复【注册】试试吧。'
    staff = User.objects.get(openid=openid)
    today_date = datetime.date.today()
    staff_sign = StaffSignRecord.objects.filter(staff=staff, date__month=today_date.month).order_by('-date')

    welcome = u'早上好，'
    today_date_string = u'%s年%s月%s日' % (today_date.year, today_date.month, today_date.day)
    weekday = get_week_day(today_date.weekday())
    now_time_string = u'%s点%s分' % (datetime.datetime.today().hour, datetime.datetime.today().minute)
    is_success = u'今日打卡成功'
    sign_num = len(staff_sign) + 1

    every_day_say = u'加油！'

    if not staff_sign:
        s = StaffSignRecord(staff=staff)
        s.save()

    else:
        last_sign_date_time = staff_sign[0].date
        last_sign_date = last_sign_date_time.date()
        today_date = datetime.date.today()
        delta_days = (today_date-last_sign_date).days
        if delta_days == 0:
            return u'你今天已经签过到了，请勿重复签到！'
        elif delta_days == 1:
            continue_sign = staff_sign[0].continue_sign+1
            s = StaffSignRecord(staff=staff, continue_sign=continue_sign)
            s.save()
        else:
            s = StaffSignRecord(staff=staff)
            s.save()

    h = s.date.time().hour
    m = s.date.time().minute
    if h > 8 and m > 0:
        is_success = u'今天好像迟到了哦'
        s.is_late = True
        s.save()
    if h > 9:
        welcome = ''



    return u'%s今天是%s %s，现在时间是%s，%s，这是本月第%s次打卡。%s' % (welcome, today_date_string, weekday, now_time_string, is_success, sign_num, every_day_say)