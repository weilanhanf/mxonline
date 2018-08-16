from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComment, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.

class CourseListView(View):
    """
    课程列表页
    """
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        # 搜索功能
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            # 对指定字段进行匹配  带i的一般不区分大小写
            all_courses = all_courses.filter(Q(desc__icontains=search_keywords) |
                                             Q(name__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))

        # 按照学习人数或者点击量分类
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by('-students')
            elif sort == "hot":
                all_courses = all_courses.order_by('-click_nums')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request, 'course/course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 用户点击量操作
        course.click_nums += 1
        course.save()

        # 是否收藏
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=course.id):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course.course_org.id):
                has_fav_org = True

        # 根据课程标签做相关课程推荐
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []

        return render(request, 'course/course-detail.html', {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_org": has_fav_org,
            "has_fav_course": has_fav_course,
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程学习页面：章节， 资源
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.students += 1
        course.save()

        # 课程相关资源
        all_resource = CourseResource.objects.filter(course_id=int(course_id))

        # 用户课程相关联： 用户点击我要学习之后创建一条记录
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse.objects.create(user=request.user, course=course)

        # 用户相关课程推荐： 学习过该课程的同学还学习过
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses
                      if user_course.course.id != int(course_id)]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]

        return render(request, 'course/course-video.html', {
            "course": course,
            "all_resource": all_resource,
            "relate_courses": relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)

        # 课程相关资源
        all_resource = CourseResource.objects.filter(course_id=int(course_id))

        # 用户课程相关联： 用户点击我要学习之后创建一条记录
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse.objects.create(user=request.user, course=course)

        # 用户相关课程推荐
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses
                      if user_course.course.id != int(course_id)]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]

        # 课程评论
        all_comments = CourseComment.objects.filter(course=course).order_by('-add_time')
        if len(all_comments) > 8:
            all_comments = all_comments[:8]

        return render(request, 'course/course-comment.html', {
            "course": course,
            "all_comments": all_comments,
            "all_resource": all_resource,
            "relate_courses": relate_courses
        })


class VideoPlayView(LoginRequiredMixin, View):
    """
    视频播放页面
    """
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        course = video.lesson.course

        # 课程相关资源
        all_resource = CourseResource.objects.filter(course=course)

        # 用户课程相关联： 用户点击我要学习之后创建一条记录
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse.objects.create(user=request.user, course=course)

        # 用户相关课程推荐： 学习过该课程的同学还学习过
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses if user_course.course.id != int(course.id)]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]

        return render(request, 'course/course-play.html', {
            "course": course,
            "all_resource": all_resource,
            "relate_courses": relate_courses,
            "video": video,
        })


class AddCommentView(View):
    """
    添加课程评论
    """
    def post(self, request):
        # 判断登陆状态
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")

        if comments and int(course_id) > 0 :
            course_comment = CourseComment()
            course_comment.comments = comments
            course_comment.course = Course.objects.get(id=course_id)
            course_comment.user = request.user
            course_comment.save()
            return JsonResponse({'status': 'success', 'msg': '评论成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '添加评论出错'})
