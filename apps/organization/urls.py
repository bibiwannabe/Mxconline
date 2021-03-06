# coding=utf-8
__author__ = 'bibi'
__date__ = '2018/1/31 19:27'

from django.conf.urls import url


from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView
from .views import TeacherListView, TeacherDetailView
urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),

    #讲师列表页
    url(r'^teacher_list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher_detail/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name='teacher_detail'),

    url(r'^add_fav/$',AddFavView.as_view(), name='add_fav'),
]