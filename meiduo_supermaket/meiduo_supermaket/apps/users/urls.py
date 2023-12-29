from . import views
from django.urls import re_path


urlpatterns = [
    re_path(r'^register/$', views.RegisterView.as_view(), name='register'),
]