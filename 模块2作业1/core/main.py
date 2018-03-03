# -*- encoding:utf-8 -*-
# Author: Koctr

from core import search
from core import replace
from core import create
from core import remove


def run():
    """
    声明一个字典，根据用户输入语句的关键字前缀，调用对应的函数，执行SQL语句
    :return: 无
    """
    sql_prefix = {
        "select": select,
        "update": update,
        "insert": insert,
        "delete": delete,
        "exit": exit_program
    }
    print("欢迎使用员工信息管理系统，输入SQL语句管理数据，输入exit退出程序\n")
    while True:
        statement = input("SQL> ")
        sql = statement.strip()
        cmd = sql[0:6].lower()
        if cmd in sql_prefix:
            sql_prefix[cmd](sql)
        else:
            print("无效的语句\n")


def exit_program(sql):
    if sql.lower() == "exit":
        print("再见！")
        exit()


def select(sql):
    search.search(sql)


def update(sql):
    replace.update(sql)


def insert(sql):
    create.create(sql)


def delete(sql):
    remove.remove(sql)

run()