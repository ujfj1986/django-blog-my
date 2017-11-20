# -*- coding: utf-8 -*-
# Author: Jiejing Shan

from haystack.views import SearchView
from .views import BlogBasicView

class PostSearchView(SearchView, BlogBasicView):

    def extra_context(self):
        context = super(PostSearchView, self).extra_context()
        self.blogsession.update(self.request)
        context['session'] = self.blogsession
        return context
