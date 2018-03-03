# -*- coding:utf-8 -*-

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import shelve
from conf import configure as conf


class Users(object):
    '''
    用户类：
    定义了用户结构，然后存储到数据库里
    '''

    def __init__(self,name,password,total_space=5000000000,userd_space=0):
        self.name = name
        self.password = password
        self.total_space = total_space #默认配额5个G
        self.userd_space = userd_space
        if self.name == 'admin':
            self.role = 'administrator'
        else:
            self.role = 'user'


