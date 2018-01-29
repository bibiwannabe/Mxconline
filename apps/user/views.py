from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.template import RequestContext
from django.contrib.auth.hashers import make_password

from .forms import LoginForm, RegisterForm, ForgetForm, ModifyForm
from .models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return  None


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





