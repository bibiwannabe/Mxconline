#coding=utf-8
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm

# Create your views here.
class OrgView(View):
    def get(self,request):
        all_org = CourseOrg.objects.all()
        hot_org = all_org.order_by('-click_num')[0:3]
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