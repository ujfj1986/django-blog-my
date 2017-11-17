# -*- coding: utf-8 -*-
# Author: Jiejing Shan
from django.shortcuts import render, get_object_or_404, redirect
import markdown

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Category, Tag
from comment.forms import CommentForm
from .blogsession import BlogSession
from django.views.generic import ListView, DetailView
from .views import BlogBasicView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

import logging

logger = logging.getLogger('blog.views')

class PostDetailView(DetailView, BlogBasicView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        #logger.error("in PostDetailView.get.")
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        #logger.error("after supper")

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
        self.blogsession.update(request)

        # 视图必须返回一个 HttpResponse 对象
        return response

    '''def get_queryset(self):
        logger.error("in get_queryset.")
        return super(DetailView, self).get_queryset()'''

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        #logger.error("in get_object, %s." % queryset)
        post = super(PostDetailView, self).get_object(queryset=None)
        #logger.error("after get_object super. post is %s." % Post)
        md = markdown.Markdown(extensions=[
                              'markdown.extensions.extra',
                              'markdown.extensions.codehilite',
                              TocExtension(slugify = slugify),
                              ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        pk = self.kwargs.get('pk')
        #logger.error("pk is %s." % pk)
        post.before = Post.objects.filter(pk=str(int(pk)-1)).first()
        post.next = Post.objects.filter(pk=str(int(pk)+1)).first()
        #logger.error("post.tags is %s." % post.tags.all().first())
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        #logger.error("in get_context_data." )
        context = super(PostDetailView, self).get_context_data(**kwargs)
        #logger.error("after get_context_data super.")
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
            'session': self.blogsession
        })
        return context
