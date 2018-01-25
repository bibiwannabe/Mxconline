# coding=utf-8
__author__ = 'bibi'
__date__ = '2018/1/25 18:05'

import xadmin


from .models import CityDict, CourseOrg, Teacher

class CityDictAdmin(object):
    list_display = ['name', 'decs', 'add_time']
    search_fields = ['name', 'decs']
    list_filter = ['name', 'decs', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'fav_num','image','add','city','add_time']
    search_fields = ['name', 'desc', 'fav_num','image','add','city__name']
    list_filter = ['name', 'desc', 'fav_num','image','add','city__name','add_time']

class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_year', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']
    search_fields = ['name', 'org', 'work_year', 'work_company', 'work_position', 'points', 'click_num', 'fav_num']
    list_filter = ['name', 'org', 'work_year', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']


xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(Teacher,TeacherAdmin)