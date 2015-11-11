# -*- coding: utf-8 -*-

from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class RegistForm(forms.Form):
    # name = forms.CharField(label=u'姓名', max_length=5, initial='aaa', widget=forms.TextInput(attrs={'id': 'myFIELD'}))
    name = forms.CharField(label=u'姓名', max_length=5, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    phonenumber = forms.CharField(label=u'手机号', max_length=12, widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    verification_code = forms.CharField(label=u'验证码', max_length=6, widget=forms.TextInput(attrs={'class':'form-control', 'style':'width:120px;float:left;margin-right: 10px;'}), required=True)

    # error_css_class = 'error'
    # required_css_class = 'required'