from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
#from ..blog.blogsession import BlogSession

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

    model = User
    template_name = 'blog/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        form = LoginForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        cur_path = kwargs.get('cur_path')
        logger.error("cur_path is %s." % cur_path)
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = User.objects.get(form.username)
                