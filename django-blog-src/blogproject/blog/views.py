from django.shortcuts import render, get_object_or_404
import markdown

# Create your views here.
from django.http import HttpResponse
from .models import Post, Category, Tag
from comment.forms import CommentForm

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context= {
            'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                 extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                 ])
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

def get_post_by_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=category)
    return render(request, 'blog/index.html', context= {
            'post_list': post_list})

def get_posts_by_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, 'blog/index.html', context={
            'post_list': post_list})