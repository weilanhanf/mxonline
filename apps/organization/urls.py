# -*- coding: utf-8 -*-

from django.conf.urls import url

# from .views import OrgView, UserAskView, OrgHomeView, OrgCourseView, OrgTeacherView, OrgDescView
from .views import *


app_name = "organization"

urlpatterns = [

    # 课程机构列表
    url(r'^list/$', OrgView.as_view(), name="org_list"),

    # 用户咨询表单
    url(r'^add_ask/$', UserAskView.as_view(), name="add_ask"),

    # 机构首页
    url(r'home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name="org_home"),

    # 课程机构列表
    url(r'course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name="org_course"),

    # 机构讲师页
    url(r'teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name="org_teacher"),

    # 机构详情页
    url(r'desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name="org_desc"),

    # 收藏，取消收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),

    # 所有教师列表
    url(r'teacher/list/$', TeacherListView.as_view(), name="teacher_list"),

    # 讲师详情页
    url(r'teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]
