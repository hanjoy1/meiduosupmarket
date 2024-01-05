from . import views
from django.urls import re_path


urlpatterns = [
    re_path(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否重复
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountview.as_view()),

    # 判断
    re_path(r'^login/$', views.LoginView.as_view(), name='login'),
    # 退出用户
    re_path(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # 用户中心
    re_path(r'^info/$', views.UserInfoView.as_view(), name='info'),
    # 添加邮箱
    re_path(r'^emails/$', views.EmailView.as_view()),
]