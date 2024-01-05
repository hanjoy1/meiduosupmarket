from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpRequest
from django import http
import re, json, logging
from users.models import User
from django.db import DatabaseError
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from meiduo_supermaket.utils.response_code import RETCODE
from django.contrib.auth.mixins import LoginRequiredMixin
from meiduo_supermaket.utils.views import LoginRequiredJSONMixin
# Create your views here.


# 创建日志输出
logger = logging.getLogger('django')
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
        response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
        # 响应结果
        return response


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

class LoginView(View):
    def post(self, request):
        # 接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        # 校验参数
        if not all([username, password]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('密码最少为8位，最长为20位')
        # 认证用户： 使用账号查询用户是否存在， 如果用户存在 再校验密码是否正确
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg':'账号或者密码错误'})
        # 状态保持
        login(request, user)
        # 使用remembered确定状态保持周期长短
        if remembered != 'on':
            # 没有记住的话， 状态保持在会话结束后就销毁
            request.session.set_expiry(0)
        else:
            # 记住登录： 状态保持一定时间 两周 默认是两周
            request.session.set_expiry(None)
        #为了实现右上角展示用户的信息, 我们需要将用户名缓存到cookie中
        # response.set_cookie('key', 'val', 'expiry')
        next = request.GET.get('next')
        if next:
            response = redirect(next)
        else:
            response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 14)
        # 响应结果
        return response

    def get(self, request):
        return render(request, 'login.html')

class LogoutView(View):
    """ 用户退出 """
    def get(self, requset):
        """" 实现用户退出登录 """
        # 清除状态保持信息
        logout(requset)
        # 删除cookie中的用户名
        response =  redirect(reverse('contents:index'))
        response.delete_cookie('username')
        # 响应结果
        return response


class  UserInfoView(LoginRequiredMixin, View):
    """ 用户中心 """
    def get(self, requset):
        """ 提供用户中心页面 """
        # if requset.user.is_authenticated:
        #     return render(requset, 'user_center_info.html')
        # else:
        #     return redirect(reverse('users:login'))
        # 如果LoginRequireMixin 判断出用户已经登录 ， 那么request.user 就是登录的用户
        context = {
            'username': requset.user.username,
            'mobile': requset.user.mobile,
            'email': requset.user.email,
            'email_active': requset.user.email_active,
        }

        return render(requset, 'user_center_info.html', context)


    # 添加邮箱
class EmailView(LoginRequiredJSONMixin, View):
    def put(self, request):
        # 接受参数
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get('email')
        # 校验参数
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数email有误')
        # 将用户写入的邮箱保存到用户数据库当中的email字段中
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg':'添加邮箱失败'})
        # 发送邮箱验证

        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg':'OK'})

