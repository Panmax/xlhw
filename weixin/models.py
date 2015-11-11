# -*- coding: utf-8 -*-

from django.db import models


class Commander(models.Model):
    commander = models.CharField(u'回复指令', max_length=10)

    def __unicode__(self):
        return self.commander

    class Meta:
        verbose_name_plural = u'回复指令管理'


class News(models.Model):
    title = models.CharField(u'标题', max_length=50)
    description = models.CharField(u'描述', max_length=100)
    picurl = models.URLField(u'图片地址')
    contenturl = models.URLField(u'内容地址')
    commander = models.ForeignKey(Commander, verbose_name=u'回复指令')
    priority = models.IntegerField(u'优先级')

    is_valid = models.BooleanField(u'有效', default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = u'图文消息'


class Text(models.Model):
    content = models.TextField(u'回复内容', max_length=100)
    commander = models.ForeignKey(Commander, verbose_name=u'回复指令')

    is_valid = models.BooleanField(u'有效', default=True)

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name_plural = u'文本消息'

class User(models.Model):
    openid = models.CharField(max_length=50, unique=True)
    name = models.CharField(u'姓名', max_length=10)
    phonenumber = models.CharField(u'手机号', max_length=12)
    reg_date = models.DateTimeField(u'注册时间', auto_now_add=True, )

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.phonenumber

    # def get_absolute_url(self):
    #     return "/user/myvip/%s" % self.openid

    class Meta:
        verbose_name_plural = u'用户'

class SendDynamicRecord(models.Model):
    openid = models.CharField(max_length=50)
    phonenumber = models.CharField(u'手机号', max_length=12)
    password = models.CharField(u'随机码', max_length=5)
    send_date = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __unicode__(self):
        return self.password

class PhonePaste(models.Model):
    user = models.ForeignKey(User)
    remain = models.IntegerField()

class PhonePasteRecoder(models.Model):
    user = models.ForeignKey(User)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class PhonePasteTransfer(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class PhonePasteRechargeRecord(models.Model):
    user = models.ForeignKey(User, related_name='user')
    updater = models.ForeignKey(User, related_name='updater')
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

class StaffSignRecord(models.Model):
    staff = models.ForeignKey(User)
    continue_sign = models.IntegerField(u'连续签到', default=1)
    date = models.DateTimeField(auto_now=True)
    is_late = models.BooleanField(default=False)
