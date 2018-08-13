from __future__ import unicode_literals

from datetime import datetime

from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市名")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    """
    课程机构
    """
    CATEGORY_CHOICE = (
        ('pxjg', "培训机构"),
        ('xx', '学校'),
        ('gr', '个人'),
    )
    city = models.ForeignKey(City, verbose_name=u"所在城市", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    category = models.CharField(verbose_name="机构类别", max_length=30, choices=CATEGORY_CHOICE, default="xx")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u"Logo")
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def get_class_course(self):
        return self.course_set.order_by('-students')[:2]

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"教师名")
    work_years = models.IntegerField(default=0, verbose_name=u"工作年限", null=True, blank=True)
    work_company = models.CharField(max_length=50, verbose_name=u"就职公司", null=True, blank=True)
    # 如果模型字段设置blank=True，那么表单字段的required设置为False 。否则，required = True
    work_position = models.CharField(max_length=50, verbose_name=u"公司职位", null=True, blank=True)
    points = models.CharField(max_length=50, verbose_name=u"教学特点", null=True, blank=True)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fanv_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name=u"头像", null=True, blank=True)
    age = models.IntegerField(verbose_name="年龄", default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_num(self):
        return self.course_set.count()
