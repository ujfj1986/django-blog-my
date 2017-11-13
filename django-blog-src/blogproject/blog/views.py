from django.shortcuts import render, get_object_or_404
import markdown

# Create your views here.
from django.http import HttpResponse
from .models import Post, Category, Tag
from comment.forms import CommentForm
from .blogsession import BlogSession
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

from django.views.generic import ListView
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    blogsession = BlogSession()

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
        return context

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