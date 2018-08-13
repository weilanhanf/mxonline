from __future__ import unicode_literals

from datetime import datetime

# 第三方models
from django.db import models
from django.contrib.auth.models import AbstractUser
# 继承djangp自带auto_models表的字段的基础上加入新的字段

# 自定义models

# Create your models here.


class UserProfile(AbstractUser):

    '''
    def get_user_name(self):
        return self.username
    nick_name_default = get_user_name()
    '''

    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default='')
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)  # 默认为空，表单验证时也可以为空
    gender = models.CharField(verbose_name="性别", max_length=6, choices=(("male", u"男"), ("female", u"女")), default="male")
    address = models.CharField(verbose_name="住址", max_length=100, default=u"", null=True, blank=True)
    mobile = models.CharField(verbose_name="联系方式", max_length=11, null=True, blank=True)
    '''
    如果你的  MEDIA_ROOT  设定为  '/home/media'  ，并且  upload_to  设定
    为  'photos/%Y/%m/%d'  。  upload_to  的 '%Y/%m/%d'  被 strftime()  所格式
    化； '%Y'  将会被格式化为一个四位数的年份,  '%m'  被格式化为一个两位数的
    月份 '%d'  是两位数日份。如果你在Jan.15.2007上传了一个文件，它将被保存
    在 /home/media/photos/2007/01/15  目录下
    '''
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=100, null=True, blank=True)

    class Meta:
        # 给模型类赋予一个更可读的名字
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def unread_message(self):
        # 获取当前用户未读消息数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id).count()


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码
    """
    SEND_CHOICES =(
        ("register", u"注册"),
        ("forget", u"找回密码"),
        ("update_email", "修改邮箱")
    )
    code = models.CharField(max_length=50, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(choices=SEND_CHOICES, max_length=20, verbose_name="发送类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")
    # 将now()中的括号去掉保证默认时间是models实例化的时间，而不是编译时间

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    # 存储在数据库中的是图片的保存地址，需要max——length
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")  # 记录生成时间

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title