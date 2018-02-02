# coding=utf-8
__author__ = 'bibi'
__date__ = '2018/2/2 11:07'


from django.conf.urls import url
from .views import CourseListView,CourseDetailView


#from .views import

urlpatterns = [
    url(r'^list/$',CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
]