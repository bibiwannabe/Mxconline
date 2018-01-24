#coding=utf-8
from django.db import models
from datetime import datetime

#from organization.models import CourseOrg

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2, verbose_name=u'难度级别')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟）')
    student = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name=u'封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u'课程点击量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
 #   organization = models.ForeignKey(CourseOrg, verbose_name=u'机构', on_delete=False)

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'课程名')
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=False)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程章节'
        verbose_name_plural = verbose_name


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    lesson = models.ForeignKey(Lesson, verbose_name=u'课程', on_delete=False)

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

class CourseResource(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'资料名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=False)

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name