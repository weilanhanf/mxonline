# -*- coding: utf-8 -*-
import xadmin

from .models import CourseOrg, City, Teacher


class CourseOrgAdmin(object):
    """"机构"""

    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'city', 'address', 'add_time']
    # 设置可以被外键搜索替代纯下拉框
    relfield_style = 'fk-ajax'


class CityAdmin(object):
    """城市"""

    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class TeacherAdmin(object):
    """
    老师
    """
    list_display = ['name', 'org', 'work_years', 'work_company', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'click_nums', 'fanv_nums', 'add_time']


xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
