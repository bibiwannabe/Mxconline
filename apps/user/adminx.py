# coding=utf-8
__author__ = 'bibi'
__date__ = '2018/1/25 13:05'

from datetime import datetime
from django.db import models
from xadmin import views

import xadmin



from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = 'MX后台管理系统'
    site_footer = 'Mx在线'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u'轮播图', max_length=100)
    url = models.URLField(max_length=200, verbose_name=u'访问地址')
    order = models.IntegerField(default=100, verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    list_display = ['title', 'image', 'url', 'order', 'add_time' ]
    search_fields = ['title', 'image', 'url', 'order']
    list_filter = ['title', 'image', 'url', 'order', 'add_time' ]

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)