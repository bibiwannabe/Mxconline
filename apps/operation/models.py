#coding=utf-8
from django.db import models

from datetime import datetime

from coursers.models import Course
from user.models import UserProfile
from organization.models import Teacher, CourseOrg


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11, verbose_name=u'手机')
    course_name = models.CharField(max_length=50, verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程咨询'
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    course = models.ForeignKey(Course,on_delete=False, verbose_name=u'课程')
    user = models.ForeignKey(UserProfile, on_delete=False, verbose_name=u'用户')
    comment = models.CharField(max_length=200, verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=False, verbose_name=u'用户')
    fav_id = models.IntegerField(default=0, verbose_name=u'数据id')
    fav_type = models.IntegerField(choices=((1, u'课程'), (2, u'课程机构'), (3, u'讲师')), default=1, verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'用户ID')
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=False, verbose_name=u'用户')
    course = models.ForeignKey(Course, on_delete=False, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name