# author: Jiejing Shan
# -*- code: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'login'

urlpatterns = [
    url(r'^login/(?:next=(?P<path>^/\w+$))$', views.login, name='login'),
]