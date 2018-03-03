#-*- coding:utf-8 -*-
'''
配置文件

'''

import os
import sys
import platform
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
if platform.system() == "Windows":
    BASE_DIR = "\\".join(os.path.abspath(os.path.dirname(__file__)).split("\\")[:-1])
    #print(BASE_DIR)
    DB_PATH = os.path.join(BASE_DIR,"db")
    #print(DB_PATH)
else:
    BASE_DIR = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
    DB_PATH = os.path.join(BASE_DIR, "db")
    #print(DB_PATH)

admin_db_filepath = os.path.join(DB_PATH,"admin")     #管理员数据库存放目录
users_db_filepath  = os.path.join(DB_PATH,"uesrs")    #普通用户数据库存放目录

FTP_BASE = os.path.join(BASE_DIR,'ftpfiles')#ftp基本目录

SERVER_IPPORT = ("127.0.0.1",9999)