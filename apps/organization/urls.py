# coding=utf-8
__author__ = 'bibi'
__date__ = '2018/1/31 19:27'

from django.conf.urls import url


from .views import OrgView, AddUserAskView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'add_ask/$', AddUserAskView.as_view(), name='add_ask')
]