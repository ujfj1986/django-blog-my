# author: Jiejing Shan
# -*- code: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^index.html$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.get_posts_by_tag, name='tag'),
]