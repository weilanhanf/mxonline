"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView  # 模板处理
from django.views.static import serve  # 上传文件处理函数
import xadmin

from users.views import IndexView, LoginView, LogoutView, RegisterView, \
                        ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from MxOnline.settings import MEDIA_ROOT, STATICFILES_DIRS


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # path('login/', TemplateView.as_view(template_name="login.html"), name = "login"),
    path('', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify/$', ModifyPwdView.as_view(), name="modify_pwd"),

    # 配置验证码相关
    url('captcha/', include('captcha.urls')),

    # 机构url配置
    url(r'^org/', include("organization.urls", namespace="org")),

    # 课程url配置
    url(r'^course/', include("course.urls", namespace="course")),

    # 用户中心相关配置
    url(r'^users/', include("users.urls", namespace="users")),

    # 配置上传文件的处理函数
    url(r'^media/(?P<path>.*$)', serve, {"document_root": MEDIA_ROOT}),

    #
    # url(r'^static/(?P<path>.*$)', serve, {"document_root": STATICFILES_DIRS}, name='static'),

    # 富文本url配置
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]


# 全局404页面配置
handler404 = 'users.views.page_not_found'
# 全局500页面
handler500 = 'users.views.page_error'
