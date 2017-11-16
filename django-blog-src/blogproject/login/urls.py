# author: Jiejing Shan
# -*- code: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'login'

urlpatterns = [
    url(r'^login/next=(?P<cur_path>([a-z0-9\W]+?))$', views.LoginView.as_view(), name='login'),
    url(r'^logout/next=(?P<cur_path>([a-z0-9\W]+?))$', views.logout, name='logout'),
]