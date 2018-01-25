# coding=utf-8
__author__ = 'bibi'
__date__ = '2018/1/25 18:17'

import xadmin


from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse

class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user__nick_name', 'course__name']
    list_filter = ['user__nick_name', 'course__name', 'add_time']

class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name','add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name','add_time']

class CourseCommentsAdmin(object):
    list_display = ['course', 'user', 'comment', 'add_time']
    search_fields = ['course__name', 'user__nick_name', 'comment']
    list_filter = ['course__name', 'user__nick_name', 'comment', 'add_time']

class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user__nick_name', 'fav_id', 'fav_type']
    list_filter = ['user__nick_name', 'fav_id', 'fav_type', 'add_time']

class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read','add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read','add_time']

xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)