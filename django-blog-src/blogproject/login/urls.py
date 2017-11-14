# author: Jiejing Shan
# -*- code: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'login'

urlpatterns = [
    url(r'^next=(?P<cur_path>([a-z0-9/.]+))$', views.LoginView.as_view(), name='login'),
]