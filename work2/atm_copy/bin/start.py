# -*- coding:utf-8 -*-
from src import admin
from src import user

info = '''
    1.  管理员登录
    2， 用户登录
'''

print(info)
check = str(input ("选择入口>"))
if check == "1":
    admin.auth_check()
elif check == "2":
    user.run()
else:
    print("输入有误")