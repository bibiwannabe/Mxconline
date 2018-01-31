#coding=utf-8
"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
import xadmin
from django.views.generic import TemplateView
from django.views.static import serve
from Mxonline.settings import MEDIA_ROOT


from user.views import LoginView, RegisterView, ActiveUserView, ForgetView, ResetView, ModifyView



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='verication'),
    url(r'^forget/$',ForgetView.as_view(), name='forget'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset'),
    url(r'^modify/$', ModifyView.as_view(), name='modify'),

    #配置上传文件访问url
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    #课程机构url配置
    url(r'^org/',include('organization.urls', namespace='org')),
]
