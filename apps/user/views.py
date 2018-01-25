from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return  None

# Create your views here.
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        post = request.POST
        user_name = post.get('username', '')
        pass_word = post.get('password', '')
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            data = {
                'msg':'用户名或密码错误',
            }
            return render(request, 'login.html', data)
    elif request.method == 'GET':
        return render(request, 'login.html')

