# -*- coding: utf-8 -*-

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner, UserProfile


class BaseSetting(object):
    enable_themes = True  # 使用主体功能
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "MxOnline 后台管理"  # 左上角
    site_footer = "welcome to MxOnline"  # 底部
    menu_style = "accordion"  # 管理左侧菜单


class UserProfileAdmin(object):
    pass


# xadmin中这里是继承object，不再是继承admin
class EmailVerifyRecordAdmin(object):
    # 显示的列
    list_display = ['email', 'code', 'send_type', 'send_time']
    # 搜索的字段
    search_fields = ['email', 'code', 'send_type']
    # 过滤器
    list_filter = ['email', 'code', 'send_type', 'send_time']
    # model自定义图标 配置相应版本  xadmin/static/xadmin/vendor/font-awesome/css/font-awesome.css
    # model_icon = 'fa fa-address-book-o'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
# 基本配置管理与views绑定
xadmin.site.register(views.CommAdminView, GlobalSettings)
# 将title和footer信息进行注册

# xadmin.site.unregister(User)
# 注销卸载模型

# 将左侧菜单的apps名称修改  apps.py->__init__.py
# 修改xadmin相关详情页面功能xadmin/plugins/auth.py
