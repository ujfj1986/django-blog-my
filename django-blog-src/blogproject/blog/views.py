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
import logging

logger = logging.getLogger('blog.views')

def index(request):
    post_list = Post.objects.all()
    s = BlogSession(request)
    '''s = {'username': 'shjj',
        'isOwner': True,
        'isLoged': False,
        'cur_path': request.get_full_path(),
       }'''
    s.setToSession(request)
    return render(request, 'blog/index.html', context= {
            'post_list': post_list,
            'session': s})

from django.views.generic import ListView, DetailView
class BlogBasicView(object):
    blogsession = BlogSession()

class IndexView(ListView, BlogBasicView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    #blogsession = BlogSession()
    paginate_by = 10

    '''def get(self, request, *args, **kwargs):
        res = super(IndexView, self).get(request, *args, **kwargs)
        self.blogsession.update(request)
        self.blogsession.setToSession(request)
        return res'''

    def get_queryset(self):
        self.blogsession.update(self.request)
        logger.error("blogsession: %s" % self.blogsession)
        logger.error("request.session: %s"% self.request.get_full_path())
        return super(IndexView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        #self.blogsession.update(self.request)
        context['session'] = self.blogsession
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        if page_number == 1:
            right = page_range[page_number: page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            right = page_range[page_number: page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            
        data = {
            'left': left,
            'right': right,
            'right_has_more': right_has_more,
            'left_has_more': left_has_more,
            'first': first,
            'last': last,
        }
        return data

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                 extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                 ])
    post.before = Post.objects.filter(pk=str(int(pk)-1)).first()
    post.next = Post.objects.filter(pk=str(int(pk)+1)).first()
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post': post,
               'form': form,
               'comment_list': comment_list}
    return render(request, 'blog/detail.html', context=context)

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year = year,
                                    created_time__month = month)
    return render(request, 'blog/index.html', context= {
            'post_list': post_list})

class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year = year,
                                                                created_time__month = month)

def get_post_by_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=category)
    return render(request, 'blog/index.html', context= {
            'post_list': post_list})
    
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

def get_posts_by_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, 'blog/index.html', context={
            'post_list': post_list})

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
