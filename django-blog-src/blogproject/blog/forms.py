# -*- coding: utf-8 -*-
# Author: Jiejing Shan

from django import forms
from .models import Post

'''class PostForm(forms.ModelForm):
    title2 = forms.CharField()
    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'excerpt', 'body']

    def init(self, post):
        self.pk = post.pk
        self.title = post.title
        self.category = post.category
        self.tags = post.tags.all()
        self.excerpt = post.excerpt
        self.body = post.body
'''
class PostForm(forms.Form):
    title = forms.CharField(label='title')
    category = forms.CharField(label='category')
    tags = forms.CharField(label='TAGS')
    excerpt = forms.CharField(label='excerpt')
    body = forms.CharField(label='body', widget=forms.Textarea(attrs={'rows': 40,}))