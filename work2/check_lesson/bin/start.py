#-*- coding:utf-8 -*-
'''
该页面调用core/main.py用于程序的入口，进行判断设备的

'''

import os
import sys
import platform


#这种环境变量添加方法在windows环境里不生效
#ss = (os.path.dirname(os.path.dirname(__file__)))

if platform.system() == 'Windows':
    BASE_DIR = "\\".join(os.path.abspath(os.path.dirname(__file__)).split("\\")[:-1])
else:
    BASE_DIR = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[:-1])
sys.path.insert(0,BASE_DIR)

# ss = (os.path.dirname(os.path.dirname(__file__)))
# base = "\\".join(os.path.abspath(os.path.dirname(__file__)).split("\\")[:-1])
# sys.path.insert(0,ss)
# print(sys.path)
#
# sys.path.insert(0,base)
# print(sys.path)

from core import main
from conf import configure

if __name__ == 'main':
    main.run()