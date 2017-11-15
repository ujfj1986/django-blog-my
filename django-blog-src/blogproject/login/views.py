from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
#from ..blog.blogsession import BlogSession
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from .forms import LoginForm
from blog.blogsession import BlogSession
# Create your views here.

import logging

logger = logging.getLogger('blog.views')

def login(request, cur_path):
    return HttpResponse("login")

def logout(request, cur_path):
    logger.error("cur_path is %s." % cur_path)
    session = BlogSession(request)
    session.username = None
    session.isLogined = False
    session.cur_path = cur_path
    session.setToSession(request)
    #logout(request, cur_path)
    return HttpResponseRedirect(cur_path)

class LoginView(View):

    #model = User
    template_name = 'blog/login.html'

    def get_context_data(self, **kwargs):
        #context = super(LoginView, self).get_context_data(**kwargs)
        cur_path = self.kwargs.get('cur_path')
        logger.error("in loginview get_context_data, cur_path is %s" % cur_path)
        form = LoginForm()
        context = {}
        context['form'] = form
        context['cur_path'] = cur_path
        return context

    def get(self, request, *args, **kwargs):
        #response = super(LoginView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        cur_path = kwargs.get('cur_path')
        logger.error("cur_path is %s." % cur_path)
        form = LoginForm(request.POST)
        if not form.is_valid():
            logger.error("form is not valid.")
            return HttpResponseRedirect(cur_path)
        username = request.POST['username']
        password = request.POST['password']
        logger.error("username is %s, password is %s." % (username, password))
        user = authenticate(username=username, password=password)
        if user is not None:
            logger.error("user is not None.")
            logger.error("--request's username is %s, is_authenticated is %s." % (request.user.username, request.user.is_authenticated))
            logger.error("==request.session is %s." % request.session.get('username'))
            login(request, user)
            session = BlogSession(request)
            session.username = username
            session.isLogined = True
            session.cur_path = cur_path
            session.setToSession(request)
            logger.error("request's username is %s, is_authenticated is %s." % (request.user.username, request.user.is_authenticated))
            logger.error("request.session is %s." % request.session['username'])
            #redirect() to cur_path
        else:
            logger.error("user is None.")
        return HttpResponseRedirect(cur_path)