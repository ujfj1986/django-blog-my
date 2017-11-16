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
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
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
