#-*- coding:utf-8 -*-
'''
启动ftp Client

'''
import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core import user_manage as mains


mains.run()