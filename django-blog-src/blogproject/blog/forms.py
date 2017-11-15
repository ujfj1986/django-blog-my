# -*- coding: utf-8 -*-
# Author: Jiejing Shan

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
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