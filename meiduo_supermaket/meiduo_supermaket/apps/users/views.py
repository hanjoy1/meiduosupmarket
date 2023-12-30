from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpRequest
from django import http
import re
from users.models import User
from django.db import DatabaseError
from django.urls import reverse
from django.contrib.auth import login
from meiduo_supermaket.utils.response_code import RETCODE

# Create your views here.


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """提供页面"""
        return render(request, 'register.html')

    def post(self, request):
        """实现用户的业务逻辑"""
        # 接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_re = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        # 校验参数(前后端的校验分开设计)
        # 判断参数是否齐全
        if not all([username, password, password_re, mobile, allow]):  # all校验全部元素是否有为空，有空就返回false
            return http.HttpResponseForbidden('缺少必传参数')  # '缺少必传参数，响应错误提示信息，403'
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('用户名字符数错误')
        # 判断密码是否8-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{8,20}$', password):
            return http.HttpResponseForbidden('密码字符数错误')
        # 两次密码是否一致
        if password != password_re:
            return http.HttpResponseForbidden('密码不一致')
        # 手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号不合法')
        # 用户是否勾选协议
        if allow != 'on':
            return http.HttpResponseForbidden('未勾选用户协议')
        # 保存注册信息： 核心
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            print('注册失败')
            return render(request, 'register.html', {'register_errmsg': '注册失败'})
        # 实现状态保持
        login(request, user)

        # 响应结果
        # 重定向
        return redirect(reverse('contents:index'))


class UsernameCountview(View):
    def get(self, request, username):
        """
        :param request: 请求
        :param username: 用户名
        :return: JSON
        """
        # 接受和校验参数
        # 实现主体业务逻辑: 使用username查询对应的业务条数 filter返回的满足条件的结果集
        count = User.objects.filter(username=username).count()
        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'count': count})
