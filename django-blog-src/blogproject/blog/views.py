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

from django.views.generic import ListView, DetailView
class BlogBasicView(object):
    blogsession = BlogSession()

class IndexView(ListView, BlogBasicView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    #blogsession = BlogSession()

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
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()
        self.blogsession.update(request)

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
            'session': self.blogsession
        })
        return context

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