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
> #####* 所有模型必须继承自models.Model类
> models.ForeignKey()指定一对多关系。





