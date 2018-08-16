import json

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q  # 实现复杂查找
# Q 对象可以用 & 和 | 运算符进行连接。当某个操作连接两个 Q 对象时，就会产生一个新的等价的 Q 对象。
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password  # 注册用户时对明文密码进行加密
from django.utils.safestring import mark_safe
from pure_pagination import EmptyPage, Paginator, PageNotAnInteger

from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from .models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from course.models import Course, CourseOrg, Teacher
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class IndexView(View):
    """首页"""
    def get(self, request):
        # 轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播课程
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 课程机构
        course_orgs = Course.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


class CustomBackend(ModelBackend):
    # 自定义authenticate方法 实现邮箱登录 这里需要到settings配置AUTHENTICATION_BACKENDS
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # 实现用户使用邮箱查询登录
            if user.check_password(password):
                # django后台密码为密文存储，从前端提交的密码明文无法匹配,而check_password方法可以
                return user
        except Exception as e:
            return None


class LoginView(View):
    # 用户登陆
    # 自动调用request.method,并调用相关方法 post或者get
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 如果表单验证成功，进行用户身份认真
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 调用auth模块的authenticate实现数据库用户的查找
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)  # 改变用户的登陆状态  index.html->request.user.is_authenticated
                    return redirect(reverse('index'))
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或者密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    # 用户退出
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class RegisterView(View):
    # 用户注册
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        # 实例化form对象，进行验证
        register_form = RegisterForm(request.POST)  # request.post包含从前台发送的表单
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(username=user_name):
                return render(request, "register.html", {"msg": "用户已经存在", "register_form": register_form})
            pass_word = request.POST.get('password', '')
            pass_word_story = make_password(pass_word)
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = pass_word_story
            user_profile.is_active = False
            # 将用户的is_active字段设置为False 当用户点击用于验证邮箱链接之后 完成验证 改为True 否则不能注册
            user_profile.save()

            # 当用户成功注册之后，为用户个人中心发送一条消息
            message = "欢迎您加入MxOline"
            first_message = UserMessage.objects.create(user=request.user.id, message=message)

            # 发送注册邮件
            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveUserView(View):
    # 邮箱验证码链接验证
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return HttpResponse("链接失效")

        return render(request, 'login.html')

    def post(self, request):
        pass


class ForgetPwdView(View):

    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_from": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return HttpResponse("邮件发送成功，请注意查收")
        else:
            return render(request, 'forgetpwd.html', {"forget_from": forget_form})


class ResetView(View):

    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email": email})
        else:
            html = "<p>链接失效，点击<a href='/forget/'>返回</p>"
            # return HttpResponse("链接失效")
            return HttpResponse(mark_safe(html))

        return render(request, 'login.html')


class ModifyPwdView(View):
    """
    更新密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get("email", "")
        if modify_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return render(request, 'password_reset.html', {"email": email , "modify_form": modify_form, "msg": "密码不一致"})
            password = make_password(password2)
            user = UserProfile.objects.get(email=email)
            user.password = password
            user.save()
            return redirect('/login/')
        else:
            return render(request, 'password_reset.html', {"modify_form": modify_form, "email": email})


class UserInfoView(LoginRequiredMixin, View):
    """
    用户相关信息
    """
    def get(self, request):
        return render(request, 'usercenter/usercenter-info.html')
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({'status': 'success'})
        else:
            print(json.dumps(user_info_form.errors))
            return JsonResponse({'status': 'failure', 'mobile': '非法'})
            # return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户头像上传
    """
    def post(self, request):
        # 文件上传变量放在files中
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data["image"]
            request.user.image = image
            request.user.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'})
    """
    方法二
    ModelForm 的子类可以用关键字参数 instance 接收一个已经存在的 Model 实例；
    如果使用 instance 参数，save() 将更新这个实例；如果不使用，save() 将创建一个新的 Model 实例
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            pass
    """


class UpdatePwdView(LoginRequiredMixin, View):
    """修改密码"""
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get("password1", "")
            password2 = request.POST.get("password2", "")
            if password1 != password2:
                return JsonResponse({"status": "fail", "msg": "密码不一致"})
            password = make_password(password2)
            user = request.user
            user.password = password
            user.save()
            return JsonResponse({"status": "success", "msg": "密码修改成功"})
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        # 判断用户当前填写的邮箱是否可用
        email = request.GET.get("email", "")
        if UserProfile.objects.filter(email=email):
            return JsonResponse({"email": "邮箱已被注册"})
        # 向词邮箱发送邮件
        send_register_email(email, send_type="update_email")
        return JsonResponse({"status": "success", "msg": "邮件已发送，请注意查收"})


class UpdateEmailView(LoginRequiredMixin, View):
    '''修改邮箱'''
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        # 对当前的验证码邮箱进行记录筛选
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            # 如果记录存在则修改用户邮箱
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    用户收藏课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter/usercenter-mycourse.html', {
            "user_courses": user_courses
        })


class MyFavView(LoginRequiredMixin, View):
    """我的收藏页"""
    def get(self, request):
        fav_list = []
        myfav = request.GET.get("myfav", "org")
        if myfav == "course":
            favs = UserFavorite.objects.filter(user=request.user, fav_type=1)
            for fav in favs:
                course_id = fav.fav_id
                course = Course.objects.get(id=course_id)
                fav_list.append(course)
            return render(request, 'usercenter/usercenter-fav-course.html', {
                "course_list": fav_list,
                "myfav": "course",
            })

        elif myfav == "org":
            favs = UserFavorite.objects.filter(user=request.user, fav_type=2)
            for fav in favs:
                org_id = fav.fav_id
                org = CourseOrg.objects.get(id=org_id)
                fav_list.append(org)
            return render(request, 'usercenter/usercenter-fav-course.html', {
                "org_list": fav_list,
                "myfav": "org"
            })

        elif myfav == "teacher":
            favs = UserFavorite.objects.filter(user=request.user, fav_type=3)
            for fav in favs:
                teacher_id = fav.fav_id
                teacher = Teacher.objects.get(id=teacher_id)
                fav_list.append(teacher)
            return render(request, 'usercenter/usercenter-fav-course.html', {
                "teacher_list": fav_list,
                "myfav": 'teacher'
            })


class MyMessageView(LoginRequiredMixin, View):
    """用户消息"""
    def get(self, request):
        read = request.GET.get("read", "all")
        # user字段在UserMessage表中的定义为用户的id
        user_message = UserMessage.objects.filter(user=request.user.id).order_by('-add_time')
        message_num = user_message.count()

        if read == 'yes':
            user_message = user_message.filter(has_read=True)
            message_num = user_message.count()
        elif read == 'no':
            user_message = user_message.filter(has_read=False)
            message_num = user_message.count()

        # 消息分页设置
        try:
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(user_message, 4, request=request)
        user_message = p.page(page)

        return render(request, 'usercenter/usercenter-message.html', {
            "user_message":user_message,
            "read": read,
            "message_num": message_num
        })


from django.shortcuts import render_to_response
def page_not_found(request):
    """404页面: 请求错误"""
    response = render_to_response('404.html', {})
    response.status_code = 404
    return  response


def page_error(request):
    """500页面：服务器出错"""
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response