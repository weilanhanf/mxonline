# -*- coding: utf-8 -*-
import re

from django import forms

from operation.models import UserAsk

# class UserAskForm(forms.Form):
#     name = forms.CharField(min_length=5, max_length=30, required=True, label="姓名")
#     mobile = forms.IntegerField(min_length=11, max_length=11, required=True, label="联系电话")
#     course_name = forms.CharField(min_length=5, max_length=40, required=True, label="课程名称")


class UserAskForm(forms.ModelForm):
    """
    ModelForm实现自定义字段，继承models，使用相应的字段
    """
    # my_field = forms.CharField()  # 自定义字段
    class Meta:
        model = UserAsk  # 继承相应的models
        fields = ['name', 'course_name', 'mobile']  # 使用相应的字段

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


