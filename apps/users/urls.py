# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import MyFavView, MyMessageView, MyCourseView, UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView

app_name = "users"

urlpatterns = [

    # 用户信息
    url(r"^info/$", UserInfoView.as_view(), name="user_info"),

    # 用户修改头像
    url(r"^image/upload/$", UploadImageView.as_view(), name="image_upload"),

    # 更新密码
    url(r"^update/pwd/$", UpdatePwdView.as_view(), name="update_pwd"),

    # 发送验证码
    url(r"^sendemail_code/$", SendEmailCodeView.as_view(), name="sendemail_code"),

    # 修改邮箱
    url(r"update_email/$", UpdateEmailView.as_view(), name="update_email"),

    # 用户课程
    url(r"^mycourse/$", MyCourseView.as_view(), name="my_course"),

    # 用户收藏
    url(r"^my_fav/$", MyFavView.as_view(), name="my_fav"),

    # 用户消息
    url(r"^mymessage/$", MyMessageView.as_view(), name="my_message"),
]