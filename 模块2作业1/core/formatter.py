# -*- coding:utf-8 -*-
# Author Koctr
import re

from conf import config
from core import check


def format_columns(columns):
    """
    格式化列名字符串为一个列表，转换为小写，并去掉两边的空格
    :param columns: 列名字符串，以逗号分隔 
    :return: 列名列表
    """
    table_columns = columns.lower().strip().split(',')
    for i, v in enumerate(table_columns):
        table_columns[i] = table_columns[i].strip()
    return table_columns


def format_values(table_name, table_columns, table_values):
    """
    格式化值字符串为一个列表，先去掉两边的空格，再去掉两边的双引号
    :param table_name: 表名
    :param table_columns: 列名元组，与值的顺序是一一对应的
    :param table_values: 值元组
    :return: 值列表
    """
    flag = True
    table_values_list = list(table_values)
    for value in table_values_list:
        table_values_list[table_values_list.index(value)] = value.strip()
    for column in table_columns:
        index = table_columns.index(column)
        if table_values_list[index].startswith('"') and table_values_list[index].endswith('"'):
            table_values_list[index] = table_values_list[index].strip('"')
        else:
            if int != config.TABEL_COLUMNS_TYPE[table_name][column]:
                flag = False
                print("缺失双引号")
                break
    if flag:
        return table_values_list


def generator_criteria_dict(table_name, criteria):
    """
    验证并生成条件字典，只支持>, =, like三种情况，like要转换为小写
    只验证了数字类型，没有验证手机号、日期
    :param table_name: 表名
    :param criteria: 查询条件
    :return: 查询条件字典
    """
    criteria_list = re.findall('^(.+)(>|like|=)(.+)$', criteria, flags=re.IGNORECASE)
    if criteria_list:
        column = [criteria_list[0][0].lower().strip()]
        if check.check_table_columns(table_name, column):
            value = format_values(table_name, column, [criteria_list[0][2]])
            if value:
                data_valid = check.check_data_valid(table_name, dict(zip(column, value)))
                if data_valid:
                    criteria_dict = dict()
                    criteria_dict["column"] = column[0]
                    criteria_dict["criteria"] = criteria_list[0][1].lower()
                    criteria_dict["value"] = value[0]
                    return criteria_dict
    else:
        print("不支持的条件")
