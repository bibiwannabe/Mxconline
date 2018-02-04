# coding=utf-8
__author__ = 'bibi'
__date__ = '2018/2/2 11:07'


from django.conf.urls import url
from .views import CourseListView,CourseDetailView,CourseCommentView,CourseVideoView, AddComment,VedioPlayView


#from .views import

urlpatterns = [
    url(r'^list/$',CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^video/(?P<course_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),
    url(r'^add_comment/$', AddComment.as_view(), name='add_comment'),
    url(r'video_play/(?P<video_id>\d+)/$', VedioPlayView.as_view(), name='video_play'),
]