# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CourseListView, VideoPlayView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView

app_name = 'course'

urlpatterns = [
    url(r'list/', CourseListView.as_view(), name='course_list'),

    # 课程详情页
    url('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),

    #课程信息页
    url('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),

    # 课程评论页
    url('comment/(?P<course_id>\d+)/', CourseCommentView.as_view(), name="course_comment"),

    # 添加课程评论
    url('add_comment/', AddCommentView.as_view(), name="add_comment"),

    # 课程视频
    url('video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video_play"),

]