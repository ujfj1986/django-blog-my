# author: Jiejing Shan
# -*- code: utf-8 -*-

from django.conf.urls import url
from . import views
from .feeds import AllPostsRssFeed
from .post_detail_view import PostDetailView
from .post_modify_view import PostModifyView

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^index.html$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='detail'),
    url(r'^post/(?P<pk>[0-9]+)/modify$', PostModifyView.as_view(), name='post_modify'),
    url(r'^post/add$', PostModifyView.as_view(), name='post_add'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^all/feeds/$', AllPostsRssFeed(), name='feeds'),
]