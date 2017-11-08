# django blog
---
这个文件用于记录使用django搭建blog的过程中的步骤和配置命令等。

##1. 使用python 虚拟环境

###·安装

	if python_version <= 3.4:
		pip install virtaulenv
	if python_version > 3.4:
		默认已经安装

###·创建虚拟环境

	mkdir blog_venv
	cd blog_venv
	if python_version <= 3.4:
		virtaulenv .
	if python_version > 3.4:
		python -m venv .

###·启用虚拟环境
Linux/Mac:

	source ./bin/activate

Windows:

	.\Scripts\activate.bat

正常启动后，在命令行显示上会将<code>(blog_venv)</code>添加到命令行的前面，例如：

	(blog-venv) ubuntu@ip-172-31-22-251:~/blog/blog-venv/bin$

###·关闭虚拟环境

	deactive

###.优点
隔离应用环境与主机环境，不影响其他应用。

##2. 创建blog工程

###. 安装django

	pip install django == 1.10.6

###. 创建django工程

	cd ..
	mkdir django-blog-src
	django-admin startproject blogproject
	tree blogproject	
	blogproject/
	├── blogproject
	│   ├── __init__.py
	│   ├── settings.py #django 配置文件
	│   ├── urls.py
	│   └── wsgi.py
	└── manage.py #django配置管理

###. 运行django服务

	python manage.py runserver [0.0.0.0:8000]

###. 配置django服务

	LANGUAGE_CODE = 'en-us' #配置django语言，中文为'zh-hans'
	TIME_ZONE = 'UTC' #配置django时区，'Asia/Shanghai'
	
###. 创建django APP

	python manage.py startapp blog #最后一个参数为app name
	tree blog
	blog
	├── admin.py
	├── apps.py
	├── __init__.py
	├── migrations
	│   └── __init__.py
	├── models.py
	├── tests.py
	└── views.py

##3. 创建数据库
###. 数据库设计
blog需要设计4个表：文章(Post)，分类(Category), 标签(Tag)和回复(Comment)。其中，一个文章只能有一个分类，可以有多个或者0个标签，可以有0个或者多个回复。一个回复可以是一个文章的回复，也可以是某个回复的回复。

###. 更改models
修改blog models.py文件，加入4个表的定义，主要需要注意：
> ####**所有模型必须继承自models.Model类**
> models.ForeignKey()指定一对多关系。
> models.ManyToManyField()指定多对多关系

###. 数据库迁移（创建）
在**虚拟环境**下：

	python manage.py makemigrations
	python manage.py migrate
django交互式环境：

	python manage.py shell

django创建新用户：

	python manage.py createsuperuser
	
###. 数据库访问

新建数据：
	
	>>> from blog.models import Category, Tag, Post
	>>> from django.utils import timezone
	>>> from django.contrib.auth.models import User
	
	>>> user = User.objects.get(username='myuser')
	>>> c = Category.objects.get(name='category test')
	
	>>> p = Post(title='title test', body='body test', created_time=timezone.now(), modified_time=timezone.now(), category=c, author=user)
	>>> p.save()
	
查询数据：

	Category.objects.all()
	Category.objects.get(name='category test')

>	from django.utils.six import python_2_unicode_compatible

>	# python_2_unicode_compatible 装饰器用于兼容 Python2

> 	@python_2_unicode_compatible
 
>	class Category(models.Model):
>
>	...

删除数据：

	c = Category.objects.get(name='category test')
	c.delete()

##4. Django URL与视图

###. 绑定url与视图
新建blog/urls.py文件

	blog/urls.py

	from django.conf.urls import url

	from . import views

	urlpatterns = [
    	url(r'^$', views.index, name='index'), #绑定url('')到函数views.index
	]

编写index函数：

	blog/views.py
	
	from django.http import HttpResponse
	
	def index(request):
	    return HttpResponse("欢迎访问我的博客首页！")
修改blogproject/urls.py,配置项目url:

	- from django.conf.urls import url
	+ from django.conf.urls import url, include
	from django.contrib import admin
	
	urlpatterns = [
	    url(r'^admin/', admin.site.urls),
	+   url(r'', include('blog.urls')), #参数r''表示前缀目录
	]

###视图模板
在项目根目录下新建templates/blog/目录，新建文件templates/blog/index.html,完成后目录如下：

	blogproject\
	    manage.py
	    blogproject\
	        __init__.py
	        settings.py
	        ...
	    blog\
	        __init__.py
	        models.py
	        ,,,
	    templates\
	        blog\
	            index.html

修改blogproject/settings.py文件的TEMPLATES项，设置模板路径：

	TEMPLATES = [
	    {
	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
	        'DIRS': [os.path.join(BASE_DIR, 'templates')], #设置模板路径
	        'APP_DIRS': True,
	        'OPTIONS': {
	            'context_processors': [
	                'django.template.context_processors.debug',
	                'django.template.context_processors.request',
	                'django.contrib.auth.context_processors.auth',
	                'django.contrib.messages.context_processors.messages',
	            ],
	        },
	    },
	]
	
使用render函数渲染模板：

	blog/views.py
	
	from django.http import HttpResponse
	from django.shortcuts import render
	
	def index(request):
	    return render(request, 'blog/index.html',  #参数'blog/index.html'指示文件
	    			context={ #context中的值用于替换模板中的变量
	                      'title': '我的博客首页', 
	                      'welcome': '欢迎访问我的博客首页'
	                  })
	=======
	templates/blog/index.html
	
	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>{{ title }}</title> //对应context中的title, {{ }}包括起来的叫做模板变量
	</head>
	<body>
	<h1>{{ welcome }}</h1> //对应context中的welcome
	</body>
	</html>
	
