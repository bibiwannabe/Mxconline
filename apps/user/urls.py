# coding=utf-8
__author__ = 'bibi'
__date__ = '2018/2/5 13:31'

from django.conf.urls import url


from .views import UserInfo, UploadImageView, UserInfoModifyView,SendEmailCodeView, ModifyEmailView
from .views import UserCourseView, UserFavCourseView, UserFavOrgView, UserFavTeacherView, UserMessageView


urlpatterns = [
    url(r'^info/$', UserInfo.as_view(), name='user_info'),
    url(r'^course/$', UserCourseView.as_view(), name='user_course'),
    url(r'^fav_course/$', UserFavCourseView.as_view(), name='user_fav_course'),
    url(r'^fav_org/$', UserFavOrgView.as_view(), name='user_fav_org'),
    url(r'^message/$', UserMessageView.as_view(), name='user_message'),
    url(r'^fav_teacher/$', UserFavTeacherView.as_view(), name='user_fav_teacher'),
    url(r'^msg/$', UserInfo.as_view(), name='user_msg'),
    url(r'^image/upload/$',UploadImageView.as_view(),name='image_upload'),
    url(r'^pwd/modify/$',UserInfoModifyView.as_view(),name='modiy_password'),
    url(r'^send_email_code/$',SendEmailCodeView.as_view(),name='send_email_code'),
    url(r'^email/modify/$',ModifyEmailView.as_view(),name='modify_email'),

]