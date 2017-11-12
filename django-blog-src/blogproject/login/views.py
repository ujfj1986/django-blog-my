from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse

# Create your views here.

def login(request, cur_path):
    return HttpResponse("login")

class LoginView(View):
    def get(self, request):
        return "login"

    def post(self, request):
        return "login"