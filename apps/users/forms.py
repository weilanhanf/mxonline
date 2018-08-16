# -*- coding: utf-8 -*-
import re

from django import forms
from captcha.fields import CaptchaField  # 验证码字段

from .models import UserProfile


# 前端进行简单表单验证之后，为了避免刻意的网络攻击，后台仍需验证
# 另外对表单进行验证，减少与数据库交互，减轻负担
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, max_length=20, error_messages={"required": "不可为空"})
    password2 = forms.CharField(required=True, min_length=6, max_length=20, error_messages={"required": "不可为空"})


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


class UserInfoForm(forms.ModelForm):
    """
    用户信息修改
    """
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'address' , 'birthday', 'mobile', 'gender']

    def clean_mobile(self):
        """
        验证手机号是否合法. 定义函数必须以clean_开头
        """
        mobile = self.cleaned_data['mobile']
        regex_mobile = r'^1[358]\d{9}$|^147\d{8}$|176\d{8}$'
        pattern_mobile = re.compile(regex_mobile)
        if pattern_mobile.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号非法", code="invalid mobile")