#coding=utf-8
from django.db import models
from datetime import datetime


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市名')
    decs = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=10, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'描述')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏数')
    student = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_num = models.IntegerField(default=0, verbose_name=u'课程数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'封面图')
    add = models.CharField(max_length=150, verbose_name=u'地址')
    city = models.ForeignKey(CityDict, verbose_name=u'机构城市')
    add_time = models.DateTimeField(default=datetime.now)
    tag = models.CharField(default='全国知名',max_length=20,verbose_name=u'机构tag')
    catgory = models.CharField(max_length=20, default='pxjg',choices=(('pxjg','培训机构'),('gr','个人'),('gx','高校')), verbose_name=u'机构类别')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_teacher_num(self):
        return self.teacher_set.all().count()



class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    name = models.CharField(max_length=50, verbose_name=u'教师名称')
    work_year = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'职位')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now)
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name=u'封面图', null=True)
    age = models.IntegerField(default=20, verbose_name=u'年龄')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_course_num(self):
        return self.course_set.all().count()

    def get_latest_course(self):
        return self.course_set.all().order_by('-add_time')[:1]


