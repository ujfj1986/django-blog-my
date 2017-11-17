# -*- coding: utf-8 -*-
# Author: Jiejing Shan
from django.shortcuts import render, get_object_or_404, redirect
import markdown

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Category, Tag
from comment.forms import CommentForm
from .blogsession import BlogSession
from .forms import PostForm
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .views import BlogBasicView
import logging

logger = logging.getLogger('blog.views')

class PostModifyView(DetailView, BlogBasicView):
    model= Post
    template_name = 'blog/post_modify.html'
    context_object_name = 'form'

    def get(self, request, *args, **kwargs):
        self.blogsession.update(request)
        cur_path = request.get_full_path()
        if self.blogsession.isLogined:
            return super(PostModifyView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect('/login/next=%s' % cur_path)

    def get_object(self, queryset = None):
        path = self.request.get_full_path()
        form = PostForm()
        if path.endswith('modify'):
            pk = self.kwargs.get('pk')
            post = super(PostModifyView, self).get_object(queryset=None)
            tags_list = post.tags.all()
            tag_str = ''
            for tag in tags_list:
                tag_str += tag.name + ' '
            form = PostForm(initial = {
                'title': post.title,
                'category': post.category,
                'tags': tag_str,
                'excerpt': post.excerpt,
                'body': post.body,
            })
            #form.fields['title'] = post.title + 'ddd'
            form.pk = post.pk
            #form.init(post)
            form.is_modify = True
        else :
            form.is_modify = False
        return form

    def get_context_data(self, **kwargs):
        self.blogsession.update(self.request)
        context = super(PostModifyView, self).get_context_data(**kwargs)
        context['session'] = self.blogsession
        return context

    def post(self, request, *args, **kwargs):
        self.blogsession.update(request)
        logger.error("user is %s." % self.blogsession.username)
        cur_path=request.get_full_path()
        if not self.blogsession.isLogined:
            return HttpResponseRedirect('/login/next=%s' % cur_path)
        form = PostForm(request.POST)
        if not form.is_valid():
            return HttpResponseRedirect(cur_path)
        post = None
        if cur_path.endswith('modify'):
            pk = kwargs.get('pk')
            post = Post.objects.get(pk=pk)
        else:
            post = Post()
            post.created_time = now()
            user = User.objects.get(username=self.blogsession.username)
            logger.error("--- user is %s." % user.username)
            post.author = user
        post.title = form.cleaned_data['title']
        post.excerpt = form.cleaned_data['excerpt']
        cate = Category.objects.all().filter(name=form.cleaned_data['category']).first()
        if cate is None:
            cate = Category(name=form.cleaned_data['category'])
            cate.save()
        post.category = cate
        post.body = form.cleaned_data['body']
        post.save()
        tags_str = form.cleaned_data['tags']
        old_tags = []
        if post.tags is not None:
            old_tags = post.tags.all()
        logger.error("post new tags: %s." % tags_str)
        logger.error("post old tags:")
        for tag in old_tags:
            logger.error(tag.name)
        tag_obj = None
        for tag in tags_str.split(' '):
            if tag is None:
                continue
            logger.error("tag is %s." % tag)
            tag_obj = Tag.objects.all().filter(name=tag).first()
            if tag_obj is None:
                tag_obj = Tag(name=tag)
                tag_obj.save()
            if post.tags is None:
                post.tags.create(tag_obj)
                continue
            if tag_obj in post.tags.all():
                continue
            post.tags.add(tag_obj)
        for tag in old_tags:
            if tag.name in tags_str:
                continue
            post.tags.remove(tag)
        post.save()
        return redirect(post)
