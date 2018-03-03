#-*- coding:utf-8 -*-
'''
配置文件

'''

import os
import sys
import platform

if platform.system() == "Windows":
    BASE_DIR = "\\".join(os.path.abspath(os.path.dirname(__file__)).split("\\")[:-1])
    #print(BASE_DIR)
    DB_PATH = os.path.join(BASE_DIR,"db")
    #print(DB_PATH)
else:
    BASE_DIR = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
    DB_PATH = os.path.join(BASE_DIR, "db")
    #print(DB_PATH)

school_db_filepath = os.path.join(DB_PATH,"school")
student_db_filepath  = os.path.join(DB_PATH,"student")