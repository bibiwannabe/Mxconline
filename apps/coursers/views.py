#coding=utf-8
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import Course, Lesson, Video
from organization.models import CourseOrg
from operation.models import CourseComments, UserFavorite, UserCourse


# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')
        hot_course = Course.objects.filter().order_by('-click_nums')[0:3]
        search_key = request.GET.get('keywords','')
        if search_key:
            all_course = Course.objects.filter(Q(name__icontains=search_key)|Q(desc__icontains=search_key)|Q(detail__icontains=search_key))
        sort = request.GET.get('sort','')
        if sort == 'hot':
            all_course = all_course.order_by('-click_nums')
        if sort == 'student':
            all_course = all_course.order_by('-student')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_course, request=request, per_page=9)
        course = p.page(page)

        data = {
            'all_course': course,
            'hot_course': hot_course,
            'sort':sort,
            'search_key':search_key,
        }
        return render(request,'course-list.html', data)


class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums = course.click_nums + 1
        course.save()
        org = CourseOrg.objects.get(id=course.org_id)
        has_fav_org = False
        has_fav_course = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.org_id), fav_type=2):
                has_fav_org = True

        recommend = []
        if course.tag:
            recommend = Course.objects.filter(tag=course.tag).order_by('-click_nums')[:1]
        data = {
            'course':course,
            'org':org,
            'recommend':recommend,
            'has_fav_org': has_fav_org,
            'has_fav_course':has_fav_course,
        }
        return render(request, 'course-detail.html', data)


class CourseVideoView(LoginRequiredMixin, View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        has_learned = UserCourse.objects.filter(user=request.user,course=course)
        if not has_learned:
            usercourse = UserCourse(user=request.user, course=course)
            usercourse.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        all_courses_id = [user_course.course_id for user_course in all_user_courses]
        other_courses = Course.objects.filter(id__in=all_courses_id).order_by('-click_nums')[:3]
        all_lesson = Lesson.objects.filter(course_id=int(course_id))
        org = CourseOrg.objects.get(id=course.org_id)

        data = {
            'course':course,
            'org':org,
            'all_lesson':all_lesson,
            'other_courses':other_courses,
        }
        return render(request, 'course-video.html', data)


class CourseCommentView(LoginRequiredMixin, View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        all_courses_id = [user_course.course_id for user_course in all_user_courses]
        other_courses = Course.objects.filter(id__in=all_courses_id).order_by('-click_nums')[:3]
        all_comment = CourseComments.objects.filter(course=int(course_id)).order_by('-add_time')
        org = CourseOrg.objects.get(id=course.org_id)

        data = {
            'course':course,
            'org':org,
            'all_comments': all_comment,
            'other_courses': other_courses,
        }
        return render(request, 'course-comment.html', data)


class AddComment(View):
    def post(self,request):
        course_id = request.POST.get('course_id','')
        content = request.POST.get('comments','')
        course = Course.objects.get(id=int(course_id))
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        if Course.objects.get(id=int(course_id)):
            course = Course.objects.get(id=int(course_id))
            comment = CourseComments()
            comment.course = course
            comment.comment = content
            comment.user = request.user
            comment.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"course_id erro"}', content_type='application/json')


class VedioPlayView(View):
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        lesson = video.lesson
        course = lesson.course
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        all_courses_id = [user_course.course_id for user_course in all_user_courses]
        other_courses = Course.objects.filter(id__in=all_courses_id).order_by('-click_nums')[:3]

        data = {
            'video': video,
            'lesson':lesson,
            'course':course,
            'other_courses':other_courses,
        }
        return render(request,'course-play.html',data)



