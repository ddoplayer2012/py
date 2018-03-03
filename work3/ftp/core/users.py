# -*- coding:utf-8 -*-

import os
import sys
import shelve
from conf import configure as conf


class Users(object):
    '''
    用户类：
    '''

    def __init__(self,name,password,total_space=500000,userd_space=0):
        self.name = name
        self.password = password
        self.total_space = total_space
        self.userd_space = userd_space
        if self.name == 'admin':
            self.role = 'administrator'
        else:
            self.role = 'user'


