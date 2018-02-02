#coding=utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import Course

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

        data = {
            'course':course,
        }
        return render(request, 'course-detail.html', data)

