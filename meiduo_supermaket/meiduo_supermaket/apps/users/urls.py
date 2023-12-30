from . import views
from django.urls import re_path


urlpatterns = [
    re_path(r'^register/$', views.RegisterView.as_view(), name='register'),
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountview.as_view()),  # 判断用户名是否重复
]