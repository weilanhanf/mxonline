from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.db.models import Q

from pure_pagination import EmptyPage, Paginator, PageNotAnInteger

from .models import City, CourseOrg, Teacher
from course.models import Course
from operation.models import UserFavorite
from .forms import UserAskForm
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """

    def get(self, request):
        all_cities = City.objects.all()  # 所有的城市
        all_orgs = CourseOrg.objects.all()  # 所有的课程机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 机构搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 城市筛选
        city_id = request.GET.get("city", "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))  # 外键查询city

        # 机构筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 学习人数，课程数筛选
        sort = request.GET.get("sort", "")
        if sorted:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "course_nums":
                all_orgs = all_orgs.order_by("-course_nums")

        orgs_nums = all_orgs.count()

        # 列表分页设置
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_cities": all_cities,
            "all_orgs": orgs,
            "orgs_nums": orgs_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class UserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        if user_ask_form.is_valid():
            # 如果表单提交，modelForm直接保存数据到数据库
            """
            save() 有一个可选的 commit 关键字参数，其值为 True 或 False（默认为 True）。
            如果调用 save() 时 commit=False，那么它将返回一个还没有保存到数据库的 Model 对象。
            这种情况下，你需要调用 Model 实例本身的 save() 方法。 如果你想在保存之前自定义一些处理，
            或者你想使用特定的模型保存选项，就可以使用 commit=False。
            """
            user_ask = user_ask_form.save(commit=True)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': 'submit error'})


class OrgHomeView(View):
    """
    课程机构首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))

        # 点击量+1
        course_org.click_nums += 1
        course_org.save()

        # 反向查询到课程机构的所有课程和老师
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html', {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        })


class OrgCourseView(View):
    """
   机构课程列表页
    """
    def get(self, request, org_id):
        current_page = 'course'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    """
   机构讲师列表页
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过课程机构找到讲师。内建的变量，找到指向这个字段的外键引用
        all_teachers = course_org.teacher_set.all()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    """
   机构课程列表页
    """
    def get(self, request, org_id):
        current_page = 'desc'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddFavView(View):
    """
    收藏机构，取消收藏
    """

    def post(self, request):
        fav_id = request.POST.get("fav_id", 0)  # 具体数据哪一位讲师，机构， 课程
        fav_type = request.POST.get("fav_type", 0)  # 收藏的是哪一类型讲师，机构， 课程

        if not request.user.is_authenticated:
            # 判断用户的登陆状态，跳转登录页面由js完成
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_record:
            exist_record.delete()

            # 判断当前收藏记录的类型，并在当前记录删除之后，相应类型的收藏数-1
            if int(fav_type) == 1:
                fav_object = Course.objects.get(id=int(fav_id))

            elif int(fav_type) == 2:
                fav_object = CourseOrg.objects.get(id=int(fav_id))

            else:
                fav_object = Teacher.objects.get(id=int(fav_id))

            # 保证收藏数合法
            fav_object.fav_nums -= 1
            if fav_object.fav_nums < 0:
                fav_object.fav_nums = 0
            fav_object.save()

            return JsonResponse({'status': 'success', 'msg': '取消收藏成功'})
        else:
            if int(fav_id) > 0 and  int(fav_type) in [1, 2, 3] :
                # 当fav_id与fav_type均合法的时候才会创建收藏记录
                user_fav = UserFavorite.objects.create(user=request.user, fav_type=int(fav_type), fav_id=int(fav_id))

                # 判断当前收藏记录的类型，并在当前记录创建之后，相应类型的收藏数+1
                if int(fav_type) == 1:
                    fav_object = Course.objects.get(id=int(fav_id))

                elif int(fav_type) == 2:
                    fav_object = CourseOrg.objects.get(id=int(fav_id))

                else:
                    fav_object = Teacher.objects.get(id=int(fav_id))

                fav_object.fav_nums += 1
                fav_object.save()

                return JsonResponse({'status': 'success', 'msg': '收藏成功'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '收藏出错'})


class TeacherListView(View):
    """
    所有教师列表
    """
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teachers_num = all_teachers.count()

        # 关键词搜索
        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            # 对指定字段进行匹配  带i的一般不区分大小写
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords))

        sort = request.GET.get("sort", "")
        if sort:
            all_teachers = all_teachers.order_by("-click_nums")

        # 列表分页设置
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 5, request=request)
        teachers = p.page(page)

        # 讲师排行榜
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        return render(request, 'teachers-list.html', {
            "all_teachers": teachers,
            "teacher_num": teachers_num,
            "sort": sort,
            "hot_teachers": hot_teachers
        })


class TeacherDetailView(LoginRequiredMixin, View):
    """
    讲师详情
    """
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_course = Course.objects.filter(teacher=teacher)
        # 教师收藏和机构收藏
        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        # 分页设置
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, 5, request=request)
        all_course = p.page(page)

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html',{
            'teacher': teacher,
            'all_course': all_course,
            'sorted_teacher': sorted_teacher,
            'has_teacher_faved': has_teacher_faved,
            'has_org_faved': has_org_faved,
        })
