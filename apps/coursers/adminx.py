# coding=utf-8
__author__ = 'bibi'
__date__ = '2018/1/25 17:02'

import xadmin


from .models import Course, CourseResource, Lesson, Video


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_num', 'image', 'click_nums', 'add_time', 'org']
    search_fields = ['name', 'desc', 'detail', 'degree', 'student', 'org__name']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'student', 'fav_num', 'image', 'click_nums', 'add_time', 'org__name']


class CourseResourceAdmin(object):
    list_display = ['name', 'download', 'course', 'add_time']
    search_fields = ['name', 'download', 'course__name']
    list_filter = ['name', 'download', 'course__name', 'add_time']


class LessonAdmin(object):
    list_display = ['name', 'course', 'add_time']
    search_fields = ['name', 'course__name']
    list_filter = ['name', 'course__name', 'add_time']



class VideoAdmin(object):
    list_display = ['name', 'add_time', 'lesson']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'add_time', 'lesson']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)