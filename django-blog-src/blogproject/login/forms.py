# -*- coding: utf-8 -*-
# Author: Jiejing Shan

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput, max_length=50)