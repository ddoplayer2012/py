# -*- encoding:utf-8 -*-
# Author: Koctr


import re
import os

import core.formatter
from core import check
from core import db_handler
from core import formatter
from conf import config


def search(sql):
    """
    查询函数
    1.使用正则表达式验证关键字，分为有where和没有where两种情况
    2.验证表名
    3.如果指定列名，验证列名，如果为*，查询所有列
    4.如果有查询条件，验证查询条件
    5.进行格式化输出
    设定正则表达式，获取查询语句中select、from、where之间以及where之后的内容，
    如果内容符合要求，格式化输出staff文件中的符合要求的内容，统计输出查询到的数据行数。
    :param sql: select语句，形式类似于select * from table_name [where column1=[>|like]value1]
                                     或select column1,column2... from table_name [where column1=[>|like]value1]
    :return: 无
    """
    if "where" in sql.lower():
        query_list = re.findall("^select(.+)from(.+)where(.+)$", sql, flags=re.IGNORECASE)
    else:
        query_list = re.findall("^select(.+)from(.+)$", sql, flags=re.IGNORECASE)
    if query_list:
        table_name = query_list[0][1].strip()
        if check.check_table_name(table_name):
            columns = query_list[0][0].strip()
            if columns == '*':
                table_columns = config.TABLE_COLUMNS[table_name]
                if len(query_list[0]) == 2:
                    output(table_name, table_columns, '')
                else:
                    output(table_name, table_columns, query_list[0][2].strip())
            else:
                table_columns = formatter.format_columns(columns)
                if check.check_table_columns(table_name, table_columns):
                    if len(query_list[0]) == 2:
                        output(table_name, table_columns, '')
                    else:
                        output(table_name, table_columns, query_list[0][2].strip())
    else:
        print("无效的sql语句")


def output(table_name, table_columns, criteria):
    """
    输出行记录
    :param table_name: 表名
    :param criteria: 用户输入的查询条件字符串
    :param table_columns: 列名元组
    :return: 
    """
    if not criteria:
        file_db_format_output(table_name, table_columns, '')
    else:
        query_criteria = core.formatter.generator_criteria_dict(table_name, criteria)
        if query_criteria:
            file_db_format_output(table_name, table_columns, query_criteria)


def file_db_format_output(table_name, table_columns, query_criteria):
    """
    格式化输出文件数据表的查询结果
    :param table_name: 表名
    :param table_columns: 要输出的列元组
    :param query_criteria: 查询条件,字典
    :return: 
    """
    db_path = db_handler.db_handler(config.DATABASE)
    db_file = "%s/%s.db" % (db_path, table_name)

    if os.path.isfile(db_file):
        output_row_title(table_name, table_columns)
        output_row_line(table_name, table_columns)
        row_count = 0
        with open(db_file, 'r', encoding="utf-8") as f:
            for line in f:
                # 去掉空格和换行符，以逗号分割为一个列表
                row = line.strip().split(',')
                if query_criteria:
                    if check.is_dml_row(table_name, row, query_criteria):
                        output_rows(table_name, table_columns, row)
                        row_count += 1
                else:
                    output_rows(table_name, table_columns, row)
                    row_count += 1
        if row_count > 0:
            output_row_line(table_name, table_columns)
        print("已查询%s行" % row_count)


def output_row_title(table_name, table_columns):
    """
    输出列名作为标题
    :param table_name: 表名
    :param table_columns: 列名元组
    :return: 无
    """
    output_columns = []
    for column in table_columns:
        column_len = config.TABLE_COLUMNS_LEN[table_name][column]
        if len(column) < column_len:
            column = column.center(column_len, ' ')
        output_columns.append(column)
    print(' '.join(output_columns))


def output_row_line(table_name, table_columns):
    """
    输出行线
    :param table_name: 表名
    :param table_columns: 列名元组
    :return: 无
    """
    output_line = []
    for column in table_columns:
        column_len = config.TABLE_COLUMNS_LEN[table_name][column]
        if len(column) > column_len:
            line = ''.center(len(column), '-')
        else:
            line = ''.center(column_len, '-')
        output_line.append(line)
    print(' '.join(output_line))


def output_rows(table_name, table_columns, row):
    """
    输出行数据
    :param table_name: 表名
    :param row: 行数据元组
    :param table_columns: 要输出的列元组
    :return: 
    """
    output_row = []
    for column in table_columns:
        column_len = config.TABLE_COLUMNS_LEN[table_name][column]
        if len(column) > column_len:
            value = row[config.TABLE_COLUMNS[table_name].index(column)].center(len(column), ' ')
        else:
            value = row[config.TABLE_COLUMNS[table_name].index(column)].center(column_len, ' ')
        output_row.append(value)
    print(' '.join(output_row))
