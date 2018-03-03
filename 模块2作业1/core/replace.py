# -*- encoding:utf-8 -*-
# Author: Koctr

import re
import os

from core import check
from core import db_handler
from core import formatter
from conf import config


def update(sql):
    """
    更新函数
    1.使用正则表达式验证关键字
    2.验证表名
    3.验证更新条件
    4.格式化列与值
    5.验证要更新的列，验证值的数据类型和长度
    6.验证完整性约束：主键唯一，自增列唯一
    7.更新数据
    :param sql: update语句，格式类似于update table_name set column1=value1,column2=value2 where column1=[>|like]value1... 
    :return: 无
    """
    update_list = re.findall("^update(.+)set(.+)where(.+)$", sql, flags=re.IGNORECASE)
    if update_list:
        table_name = update_list[0][0].lower().strip()
        if check.check_table_name(table_name):
            update_criteria = formatter.generator_criteria_dict(table_name, update_list[0][2])
            if update_criteria:
                column_and_value_list = update_list[0][1].strip().split(",")
                columns = []
                values = []
                valid = True
                for item in column_and_value_list:
                    column_and_value = item.strip().split("=")
                    if len(column_and_value) == 2:
                        column = column_and_value[0].lower().strip()
                        columns.append(column)
                        value = column_and_value[1]
                        values.append(value)
                    else:
                        valid = False
                        print("sql语句错误")
                        break
                if valid:
                    if check.check_table_columns(table_name, columns) and check.check_duplicate_columns(columns):
                        values = formatter.format_values(table_name, columns, values)
                        if values:
                            if check.check_data_valid(table_name, dict(zip(columns, values))):
                                file_db_update(table_name, dict(zip(columns, values)), update_criteria)
    else:
        print("sql语句错误")


def file_db_update(table_name, columns_and_values, update_criteria):
    """
    更新表中的行数据
    :param table_name: 表名
    :param columns_and_values: 列与值的字典
    :param update_criteria: 更新条件
    :return: 无
    """
    db_path = db_handler.db_handler(config.DATABASE)
    db_file = "%s/%s.db" % (db_path, table_name)
    db_file_temp = "%s/%s.tmp" % (db_path, table_name)

    if os.path.isfile(db_file):
        count = 0
        with open(db_file, "r", encoding="utf-8") as file, open(db_file_temp, "w", encoding="utf-8") as tmp:
            flag = True
            update_rows = []
            for line in file:
                row = line.strip().split(',')
                if check.is_dml_row(table_name, row, update_criteria):
                    update_rows.append(row)
                else:
                    # 验证更新的内容是否存在主键或自增列重复（验证完整性约束）
                    if config.PRIMARY_KEY in columns_and_values:
                        if not check.check_primary_key(table_name, row, columns_and_values):
                            flag = False
                    if config.AUTO_INCREMENT in columns_and_values:
                        if not check.check_auto_increment(table_name, row, columns_and_values):
                            flag = False
                    tmp.writelines(line)
            for update_row in update_rows:
                if flag:
                    for column in columns_and_values:
                        update_row[config.TABLE_COLUMNS[table_name].index(column)] = columns_and_values[column]
                    count += 1
                tmp.writelines(','.join(update_row) + '\n')
        os.remove(db_file)
        os.rename(db_file_temp, db_file)
        print("已更新%d行" % count)
