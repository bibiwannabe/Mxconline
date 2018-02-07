#coding=utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from coursers.models import Course
from operation.models import UserFavorite

# Create your views here.
class OrgView(View):
    def get(self,request):
        all_org = CourseOrg.objects.all()
        hot_org = all_org.order_by('-click_num')[0:3]

        search_key = request.GET.get('keywords', '')
        if search_key:
            all_org = CourseOrg.objects.filter(
                Q(name__icontains=search_key) | Q(desc__icontains=search_key) )

        all_city = CityDict.objects.all()
        #城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_org = all_org.filter(city_id=int(city_id))

        #机构类型筛选
        catgory = request.GET.get('ct', '')
        if catgory:
            all_org = all_org.filter(catgory=catgory)

        sort = request.GET.get('sort','')
        if sort == 'student':
            all_org = all_org.order_by('-student')
        if sort == 'course_num':
            all_org = all_org.order_by('-course_num')

        org_num = all_org.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_org, request=request, per_page=5)
        orgs = p.page(page)

        data = {
            'all_city': all_city,
            'orgs': orgs,
            'org_num': org_num,
            'city_id':city_id,
            'catgory':catgory,
            'hot_org':hot_org,
            'sort':sort,
            'search_key':search_key,
        }
        return render(request, 'org_list.html', data)


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm((request).POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num = course_org.click_num + 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav =True
        all_course = course_org.course_set.all()[0:3]
        all_teacher = course_org.teacher_set.all()[0:1]
        data = {
            'course_org':course_org,
            'all_course':all_course,
            'all_teacher':all_teacher,
            'current_page': current_page,
            'has_fav':has_fav,

        }
        return render(request,'org-detail-homepage.html',data)


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        all_course = course_org.course_set.all()
        data = {
            'course_org': course_org,
            'all_course': all_course,
            'current_page':current_page,
            'has_fav': has_fav,

        }
        return render(request,'org-detail-course.html', data)


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        data = {
            'course_org': course_org,
            'current_page':current_page,
            'has_fav': has_fav,

        }
        return render(request,'org-detail-desc.html', data)


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        all_teacher = course_org.teacher_set.all()
        data = {
            'course_org': course_org,
            'current_page':current_page,
            'all_teacher': all_teacher,
            'has_fav': has_fav,

        }
        return render(request,'org-detail-teachers.html', data)


class AddFavView(View):
    def post(self, request):
        post = request.POST
        fav_id = post.get('fav_id', '0')
        fav_type = post.get('fav_type', '0')

        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exit_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exit_record:
            #记录存在则取消收藏
            exit_record.delete()
            if fav_type == '1':
                course = Course.objects.get(id=fav_id)
                course.fav_num-=1
                course.save()
            if fav_type == '2':
                org = CourseOrg.objects.get(id=fav_id)
                org.fav_num -= 1
                org.save()
            if fav_type == '3':
                teacher = Teacher.objects.get(id=fav_id)
                teacher.fav_num -= 1
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.user_id = request.user.id
                user_fav.save()
                if fav_type == '1':
                    course = Course.objects.get(id=fav_id)
                    course.fav_num += 1
                    course.save()
                if fav_type == '2':
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_num += 1
                    org.save()
                if fav_type == '3':
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_num += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self,request):
        all_teacher = Teacher.objects.all().order_by('-add_time')
        sorted_teacher = all_teacher.order_by('-click_num')[:3]
        search_key = request.GET.get('keywords', '')
        if search_key:
            all_teacher = Teacher.objects.filter(Q(name__icontains=search_key) | Q(work_company__icontains=search_key)
                                                 |Q(work_position__icontains=search_key))

        sort = request.GET.get('sort','')
        if sort=='hot':
            all_teacher = all_teacher.order_by('-click_num')
        teacher_num = all_teacher.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teacher, request=request, per_page=5)
        teachers = p.page(page)

        data = {
            'all_teacher': teachers,
            'sort':sort,
            'teacher_num':teacher_num,
            'sorted_teacher':sorted_teacher,
            'search_key':search_key,
        }
        return render(request,'teachers-list.html', data)


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_num = teacher.click_num+1
        teacher.save()
        all_course = Course.objects.filter(teacher_id=int(teacher_id))
        sorted_teacher = Teacher.objects.all().order_by('-click_num')[:3]
        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            fav_teacher = UserFavorite.objects.filter(user_id=request.user.id, fav_id=teacher_id, fav_type=3)
            if fav_teacher:
                has_fav_teacher = True
            fav_org = UserFavorite.objects.filter(user_id=request.user.id, fav_id=teacher.org_id, fav_type=2)
            if fav_org:
                has_fav_org = True


        data = {
            'teacher': teacher,
            'all_course': all_course,
            'sorted_teacher': sorted_teacher,
            'has_fav_org':has_fav_org,
            'has_fav_teacher':has_fav_teacher,
        }
        return render(request,'teacher-detail.html', data)



