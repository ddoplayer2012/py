# -*- encoding:utf-8 -*-
# Author: Koctr


import re
import os
from core import check
from core import db_handler
from core import formatter
from conf import config


def create(sql):
    """
    插入函数
    1.使用正则表达式验证关键字
    2.验证表名
    3.格式化列与值，如果指定列名，验证列名（去掉左右括号）
    4.验证值与列的个数是否相等
    5.验证列对应的值的数据类型和长度，自增类型的列，值为""或整数
    6.验证完整性：主键唯一，自增类型的列，如果赋值，验证列值不重复；如果未赋值，确保为已有记录中自增列的最大值+1
    7.写入数据
    注意：值要去掉双引号
    :param sql: Insert语句，格式类似于insert into table_name values(value1,value2,...)
                                     或Insert into table_name(column1,column2,...) values(value1,value2,...)
    :return: 无
    """
    insert_list = re.findall("^insert into(.+)values(.+)$", sql, flags=re.IGNORECASE)
    if insert_list:
        table_name_and_columns = re.findall("^(.+)\((.+)\)$", insert_list[0][0].strip())
        if table_name_and_columns:
            table_name = table_name_and_columns[0][0].lower().strip()
            if check.check_table_name(table_name):
                table_columns = formatter.format_columns(table_name_and_columns[0][1])
                if check.check_table_columns(table_name, table_columns) and \
                        check.check_duplicate_columns(table_columns):
                    row_write(table_name, table_columns, insert_list[0][1])
        else:
            table_name = insert_list[0][0].lower().strip()
            if check.check_table_name(table_name):
                row_write(table_name, config.TABLE_COLUMNS[table_name], insert_list[0][1])
    else:
        print("无效的sql语句")


def row_write(table_name, table_columns, insert_values):
    """
    写入行数据
    :param table_name: 表名
    :param insert_values: values关键字后面的部分
    :param table_columns: 值对应的列名元组
    :return: 
    """
    values = re.findall("^\((.+)\)$", insert_values.strip())
    if values:
        table_values = values[0].strip().split(',')
        if len(table_columns) == len(table_values):
            table_values = formatter.format_values(table_name, table_columns, table_values)
            if table_values:
                data_row = generator_insert_row(table_name, dict(zip(table_columns, table_values)))
                if data_row:
                    file_db_insert(table_name, data_row)
        elif len(table_columns) > len(table_values):
            print("值不足")
        else:
            print("值太多")
    else:
        print("值格式错误")


def file_db_insert(table_name, data_row):
    """
    验证数据完整性，验证通过后将行数据附加到文件末尾
    :param table_name: 要写入的表名
    :param data_row: 要写入的行数据元组
    :return: 无
    """
    db_path = db_handler.db_handler(config.DATABASE)
    db_file = "%s/%s.db" % (db_path, table_name)

    if os.path.isfile(db_file):
        with open(db_file, "r+", encoding="utf-8") as f:
            flag = True
            max_value = 0
            for line in f:
                row = line.strip().split(',')
                columns_and_values = dict(zip(config.TABLE_COLUMNS[table_name], data_row))
                if not check.check_primary_key(table_name, row, columns_and_values):
                    flag = False
                    break
                max_value = check.check_auto_increment(table_name, row, columns_and_values)
                if not max_value:
                    flag = False
                    break
            if flag:
                f.writelines(insert_auto_increment_column(table_name, max_value, data_row))
                print("已插入1行")


def insert_auto_increment_column(table_name, max_value, data_row):
    """
    插入自增列的列值
    :param table_name: 表名
    :param max_value: 自增列最大值
    :param data_row: 要写入的数据行元组
    :return: 无
    """
    # 传入的元组参数不能修改，需要先转换成列表
    data_row_list = list(data_row)
    if config.AUTO_INCREMENT in config.TABLE_CONSTRAINTS[table_name]:
        # 获取自增列在表中的位置索引
        increment_column_index = config.TABLE_COLUMNS[table_name]. \
            index(config.TABLE_CONSTRAINTS[table_name][config.AUTO_INCREMENT])
        # 如果数据行中自增列未赋值，自增
        if not data_row[increment_column_index]:
            data_row_list[increment_column_index] = str(int(max_value) + 1)
    return ','.join(data_row_list) + '\n'


def generator_insert_row(table_name, table_columns_and_values):
    """
    检查表中列对应值的类型、长度是否符合要求，如果符合要求，返回要写入的行数据
    只验证了数字类型，没有验证手机号、日期
    :param table_name: 表名
    :param table_columns_and_values: 列与对应值的字典 
    :return: 行数据列表
    """
    data_row = []
    # 初始化一个行数据列表，每一个元素都是''
    for i in range(len(config.TABLE_COLUMNS[table_name])):
        data_row.append('')
    data_valid = check.check_data_valid(table_name, table_columns_and_values)
    if data_valid:
        for key in table_columns_and_values:
            data_row[config.TABLE_COLUMNS[table_name].index(key)] = table_columns_and_values[key]
        return data_row
