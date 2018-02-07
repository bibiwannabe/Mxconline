#coding=utf-8
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.template import RequestContext
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
import json


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .forms import LoginForm, RegisterForm, ForgetForm, ModifyForm, UploadImageForm, UserInfoForm
from .models import UserProfile, EmailVerifyRecord, Banner
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from coursers.models import Course, CourseOrg,Teacher


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    @csrf_exempt
    def get(self, request):
        return render(request, 'login.html')

    @csrf_exempt
    def post(self, request):
        post = request.POST
        login_form = LoginForm(post)
        if login_form.is_valid():
            user_name = post.get('username', '')
            pass_word = post.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return render(request, 'login.html', {'msg': '未激活账号！'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        data = {
                    'login_form': login_form,
                }
        return render(request, 'login.html', data, context_instance=RequestContext(request))


class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html',{'register_form':register_form})

    @csrf_exempt
    def post(self, request):
        post = request.POST
        register_form = RegisterForm(post)
        if register_form.is_valid():
            email = post.get('email', '')
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'register_form':register_form,'msg':'用户已存在'})
            password = post.get('password', '')
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()

            user_message = UserMessage()
            user_message.user = user_profile
            user_message.message = '欢迎注册Mxonline'
            user_message.save()

            send_register_email(email, 'register')
            return render(request,'login.html')
        return render(request, 'register.html', {'register_form':register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request,'index.html')


class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return  render(request, 'forgetpwd.html', {'forget_form':forget_form})

    def post(self, request):
        post = request.POST
        forget_form = ForgetForm(post)
        if forget_form.is_valid():
            email = post.get('email', '')
            send_register_email(email, 'forget')
            return render(request,'send_success.html')
        return render(request,'login.html', {'forget_form':forget_form})


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,'password_reset.html',{'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request,'index.html')


class ModifyView(View):
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'msg':'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request,'login.html')
        else:
            email = request.POST.get('email', '')
            data={
                'modify_form':modify_form,
                'email':email,
            }
            return render(request,'password_reset.html', data)


class UserInfo(LoginRequiredMixin, View):
    def get(self,request):
        current_page = "info"
        user = request.user
        data = {
            'current_page':current_page,
            'user':user,
        }
        return render(request,'usercenter-info.html',data)
    def post(self,request):
        post = request.POST
        user_info_form = UserInfoForm(post, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            print('ss')
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            print(user_info_form.errors)
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin,View):
    def post(self,request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
        return HttpResponse('{"status":"success","msg":"上传成功"}')


class UserInfoModifyView(View):
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            request.user.password = make_password(pwd1)
            request.user.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self,request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status":"fail","msg":"邮箱已被注册"}', content_type='application/json')

        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class ModifyEmailView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        email = request.POST.get('email','')
        code = request.POST.get('code','')
        if EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email'):
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"验证码错误"}', content_type='application/json')


class UserCourseView(LoginRequiredMixin, View):
    def get(self,request):
        all_course = UserCourse.objects.filter(user=request.user)
        current_page = "course"
        data = {
            'all_course':all_course,
            'current_page':current_page,
        }
        return render(request,'usercenter-mycourse.html', data)


class UserFavCourseView(LoginRequiredMixin, View):
    def get(self,request):
        current_page = "fav"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        data = {
            'course_list':course_list,
            "current_page": current_page,
        }
        return render(request,'usercenter-fav-course.html',data)


class UserFavOrgView(LoginRequiredMixin, View):
    def get(self,request):
        current_page = "fav"
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        data = {
            "org_list": org_list,
            "current_page": current_page,
        }
        return render(request,'usercenter-fav-org.html', data)


class UserFavTeacherView(LoginRequiredMixin, View):
    def get(self,request):
        current_page = "fav"
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        data = {
            "teacher_list": teacher_list,
            "current_page": current_page,
        }
        return render(request, 'usercenter-fav-teacher.html', data)


class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = "message"
        all_message = UserMessage.objects.filter(Q(user=request.user.id)|Q(user=0))
        for msg in all_message:
            msg.has_read = True
            msg.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, request=request, per_page=10)
        message = p.page(page)
        data = {
            'current_page': current_page,
            'message': message,
            'page':page,
        }
        return render(request, 'usercenter-message.html',data)


class IndexView(View):
    def get(self,request):
        banner_list = Banner.objects.all().order_by('order')
        course_banner = Course.objects.filter(is_banner=True).order_by('-add_time')
        course_list = Course.objects.filter(is_banner=False).order_by('-add_time')[:6]
        org_list = CourseOrg.objects.filter().order_by('-add_time')[:15]
        data = {
            'banner_list':banner_list,
            'course_banner':course_banner,
            'course_list':course_list,
            'org_list':org_list,
        }
        return render(request,'index.html',data)

class PageNotFound(View):
    def get(self,request):
        return render(request,'404.html')


class PermissionDenied(View):
    def get(self,request):
        return render(request,'403.html')


class PageError(View):
    def get(self,request):
        return render(request,'500.html')








