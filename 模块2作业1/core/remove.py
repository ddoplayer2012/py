# -*- encoding:utf-8 -*-
# Author: Koctr


import re
import os

from core import formatter
from core import check
from core import db_handler
from conf import config


def remove(sql):
    """
    删除函数
    :param sql: delete语句，类似delete table_name where id=value 
    1.使用正则表达式验证关键字
    2.验证表名
    3.验证删除条件
    4.删除数据
    :return: 无
    """
    delete_list = re.findall("^delete(.+)where(.+)$", sql, flags=re.IGNORECASE)
    if delete_list:
        table_name = delete_list[0][0].lower().strip()
        if check.check_table_name(table_name):
            query_criteria = formatter.generator_criteria_dict(table_name, delete_list[0][1])
            if query_criteria:
                file_db_delete(table_name, query_criteria)


def file_db_delete(table_name, query_criteria):
    """
    删除表中的数据
    :param table_name: 表名
    :param query_criteria: 查询条件
    :return: 无
    """
    db_path = db_handler.db_handler(config.DATABASE)
    db_file = "%s/%s.db" % (db_path, table_name)
    db_file_tmp = "%s/%s.tmp" % (db_path, table_name)

    if os.path.isfile(db_file):
        count = 0
        with open(db_file, "r", encoding="utf-8") as file, open(db_file_tmp, "w", encoding="utf-8") as tmp:
            for line in file:
                row = line.strip().split(',')
                if check.is_dml_row(table_name, row, query_criteria):
                    count += 1
                    continue
                else:
                    tmp.writelines(line)
        os.remove(db_file)
        os.rename(db_file_tmp, db_file)
        print("已删除%d行" % count)
