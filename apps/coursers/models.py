#coding=utf-8
from django.db import models
from datetime import datetime
from organization.models import CourseOrg, Teacher

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
    org = models.ForeignKey(CourseOrg,verbose_name=u'课程机构', null=True)
    category = models.CharField(default='', max_length=20, verbose_name=u'课程类别')
    tag = models.CharField(default='',max_length=20,verbose_name=u'课程标签')
    teacher = models.ForeignKey(Teacher, null=True, verbose_name=u'讲师')
    need_know = models.CharField(max_length=300, default='', verbose_name=u'课程须知')
    what_to_learn = models.CharField(max_length=300, default='',verbose_name=u'学什么')
    is_banner = models.BooleanField(default=False,verbose_name=u'是否广告')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_zj_nums(self):
        all_lesson = self.lesson_set.all()
        return all_lesson.count()

    def get_learn_users(self):
        if self.usercourse_set.all().count()>5:
            return self.usercourse_set.all()[:5]
        else:
            return self.usercourse_set.all()

    def get_course_lesson(self):
        return self.lesson_set.all()

    def get_course_resource(self):
        return self.courseresource_set.all()

class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'章节名称')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    lesson = models.ForeignKey(Lesson, verbose_name=u'课程')
    learn_time = models.IntegerField(default=0,verbose_name=u'时长')
    url = models.CharField(max_length=200, default='', verbose_name=u'访问地址')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'资料名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    course = models.ForeignKey(Course, verbose_name=u'课程')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name