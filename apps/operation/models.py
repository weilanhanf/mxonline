from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from users.models import UserProfile
from course.models import Course

# Create your models here.


class UserAsk(models.Model):
    """用户想要学习表单"""

    name = models.CharField(max_length=20, verbose_name=u"姓名")
    mobile = models.CharField(max_length=11, verbose_name=u"手机")
    # 当字段过小的时候  不会显示搜索框
    course_name = models.CharField(max_length=50, verbose_name=u"课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}添加查询成功".format(self.name)


class CourseComment(models.Model):
    """课程评论"""

    user = models.ForeignKey(UserProfile, verbose_name=u'用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    comments = models.CharField(verbose_name=u'评论', max_length=200)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name

    def __str__(self):
       return "{0}添加《{1}》课程的评论".format(self.user, self.course)


class UserFavorite(models.Model):
    """用户收藏"""

    FAV_TYPE = (
        (1, '课程'),
        (2, '课程机构'),
        (3, '讲师'),
    )

    user = models.ForeignKey(UserProfile, verbose_name=u'用户', on_delete=models.CASCADE)
    fav_id = models.IntegerField(verbose_name=u'数据id', default=0)
    fav_type = models.IntegerField(verbose_name=u'收藏类型', choices=FAV_TYPE, default=1)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(verbose_name=u'接受用户', default=0)
    message = models.CharField(verbose_name=u'消息内容', max_length=500)
    has_read = models.BooleanField(verbose_name=u'是否已读', default=False)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    """用户课程"""
    user = models.ForeignKey(UserProfile, verbose_name=u'用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name
