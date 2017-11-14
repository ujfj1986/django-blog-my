from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
#from ..blog.blogsession import BlogSession
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from .forms import LoginForm
# Create your views here.

import logging

logger = logging.getLogger('blog.views')

def login(request, cur_path):
    return HttpResponse("login")

class LoginView(View):
    '''def get(self, request, *args, **kwargs):
        response = super(LoginView, self).get(request, *args, **kwargs)
        return response'''

    #model = User
    template_name = 'blog/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        cur_path = self.kwargs.get('cur_path')
        form = LoginForm()
        context['form'] = form
        context['cur_path'] = cur_path
        return context

    def post(self, request, *args, **kwargs):
        cur_path = kwargs.get('cur_path')
        logger.error("cur_path is %s." % cur_path)
        form = LoginForm(request.POST)
        if not form.is_valid():
            logger.error("form is not valid.")
            return HttpResponseRedirect(cur_path)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #redirect() to cur_path
        return HttpResponseRedirect(cur_path)