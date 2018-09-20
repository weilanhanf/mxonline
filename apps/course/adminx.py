# -*- coding: utf-8 -*-
import xadmin


from .models import Course, Lesson, Video, CourseResource, BannerCourse


# 必须以Inline结尾
class LessonInline(object):
    # 定义额外的嵌套表，外键指向Course
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    # 定义额外的嵌套表，外键指向Course
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    """课程"""

    # 显示的字段 get_zj_nums为自定义函数
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']  # 搜索
    # search_fields字段是不能进行时间搜索
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']  # 过滤
    # 设置默认排序
    ordering = ['-click_nums']
    # 设置只读字段
    readonly_fields = ['click_nums', 'students']
    # 设置隐藏字段 与readonly_fields功能相冲突，一个字段只能使用二者之一
    exclude = ['fanv_nums']
    # 为当前课程的详情页面添加外键关联的对象，方便数据的添加操作
    inlines = [LessonInline, CourseResourceInline]
    # 课程列表页添加字段修改功能
    list_editable = ['desc', 'degree']
    # 页面刷新时间
    refresh_times = [3, 5]
    # 对model字段相应修改为富文本编辑框
    style_fields = {"detail": "ueditor"}

    def queryset(self):
        # 重载queryset方法，来过滤出我们想要的数据的
        qs = super(CourseAdmin, self).queryset()
        # 只显示is_banner=True的课程
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        # obj实际是一个course对象
        obj = self.new_obj
        # 如果这里不保存，新增课程，统计的课程数会少一个
        obj.save()
        # 确定课程的课程机构存在。
        if obj.course_org is not None:
            # 找到添加的课程的课程机构
            course_org = obj.course_org
            # 课程机构的课程数量等于添加课程后的数量
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    """轮播课程"""

    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    model_icon = 'fa fa-book'
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        # 重载queryset方法，来过滤出我们想要的数据的
        qs = super(BannerCourseAdmin, self).queryset()
        # 只显示is_banner=True的课程
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    """章节"""

    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']
    # list_filter = ['course__name', 'name', 'add_time']
    # 这里course__name是根据课程名称过滤 外键的指定字段  如果没有则没有搜索框


class VideoAdmin(object):
    """视频"""

    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    """课程资源"""

    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


# 将后台管理器与models进行关联注册。
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
