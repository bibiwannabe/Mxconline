#coding=utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import Course, Lesson
from organization.models import CourseOrg
from operation.models import CourseComments, UserFavorite


# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')
        hot_course = Course.objects.filter().order_by('-click_nums')[0:3]
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


class CourseVideoView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_lesson = Lesson.objects.filter(course_id=int(course_id))
        org = CourseOrg.objects.get(id=course.org_id)

        data = {
            'course':course,
            'org':org,
            'all_lesson':all_lesson,
        }
        return render(request, 'course-video.html', data)


class CourseCommentView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_comment = CourseComments.objects.filter(course=int(course_id)).order_by('-add_time')
        org = CourseOrg.objects.get(id=course.org_id)

        data = {
            'course':course,
            'org':org,
            'all_comments': all_comment,
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



