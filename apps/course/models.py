from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher


# Create your models here.


class Course(models.Model):
    """课程"""
    DEGREE_CHOICE = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级'),
    )
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name="课程讲师", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    # detail = models.TextField(verbose_name=u"课程详情")
    detail = UEditorField(verbose_name='内容	', width=600, height=300, toolbars="full", imagePath="course/image/", filePath="course/image/", upload_settings={"imageMaxSize":1204000},
             settings={}, command=None, blank=True)
    degree = models.CharField(verbose_name=u"难度", choices=DEGREE_CHOICE, max_length=100)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟)")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fanv_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="course/%Y/%m", verbose_name=u"封面图", max_length=100, blank=True)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(max_length=30, default="课程类别", verbose_name="课程类别")
    tag = models.CharField(max_length=30, default="", verbose_name="课程标签")
    need_know = models.CharField(max_length=300, default="", verbose_name="课程须知")
    teacher_tell = models.CharField(max_length=300, default="", verbose_name="老师告诉你")
    is_banner = models.BooleanField('是否轮播', default=False)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取章节数
        return self.lesson_set.all().count()
    # xadmin后台课程列表页显示章节数函数的名称
    get_zj_nums.short_description = "章节数"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://www.baidu.com">跳转</a>')
    go_to.short_description = "跳转"

    def get_learn_users(self):
        # 获取当前课程5个的学习用户
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取当前课程所有的章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    """显示轮播课程"""
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        # 单例 这里必须设置proxy=True，这样就不会在生成一张表，而且具有Model的功能
        proxy = True


class Lesson(models.Model):
    """课程章节"""

    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        # 获取当前章节的所有相关学习视频
        return self.video_set.all()

    def __str__(self):
        return '《{0}》课程的章节 >> {1}'.format(self.course, self.name)


class Video(models.Model):
    """章节学习视频"""

    lesson = models.ForeignKey(Lesson, verbose_name=u"章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    learn_times = models.IntegerField(verbose_name="学习时长(分钟)", default=20)
    url = models.CharField(verbose_name="章节视频", default="", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    """课程学习资源"""

    course = models.ForeignKey(Course, verbose_name=u"章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name