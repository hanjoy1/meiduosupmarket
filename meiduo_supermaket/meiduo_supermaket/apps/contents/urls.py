from . import views
from django.urls import re_path

urlpatterns = [
    # 首页广告
    re_path(r'^$', views.IndexView.as_view(), name='index'),
]