# -*- coding: utf-8 -*-
# author: Jiejing Shan

#from django.

class BlogSession(object):
    cur_path = None
    username = None
    isOwner = False
    isLogined = False

    def __init__(self, request = None):
        if request == None :
            return
        self.username = request.session.get('username', None)
        self.isOwner = request.session.get('isOwner', False)
        self.isLogined = request.session.get('isLogined', False)
        '''self.username = request.user.username
        self.isLogined = request.user.is_authenticated'''
        self.cur_path = request.get_full_path()

    '''def __init__(self):
        pass'''

    def setToSession(self, request):
        request.session['username'] = self.username
        request.session['isOwner'] = self.isOwner
        request.session['isLogined'] = self.isLogined
        request.session['cur_path'] = self.cur_path

    def update(self, request):
        if request == None:
            return
        self.username = request.session.get('username', None)
        self.isOwner = request.session.get('isOwner', False)
        self.isLogined = request.session.get('isLogined', False)
        self.cur_path = request.get_full_path()
        self.setToSession(request)
        '''
        self.username = request.user.username
        self.isLogined = request.user.is_authenticated
        self.cur_path = request.get_full_path()'''


    def __str__(self):
        return '{username: %s, isOwner: %s, isLogined: %s, cur_path: %s}' % (self.username, self.isOwner, self.isLogined, self.cur_path)
        