# -*- encoding:utf-8 -*-
# Author: Koctr


from conf import config


def is_dml_row(table_name, row, query_criteria):
    """
    声明一个字典，根据查询条件调用对应函数，判断此行是否执行dml操作
    :param table_name: 表名
    :param row: 行数据元组
    :param query_criteria: 查询条件字典
    :return: 判断结果
    """
    compare_dict = {
        ">": granter_than,
        "=": equals,
        "like": like,
    }
    if query_criteria["criteria"] in compare_dict:
        # print(row[config.TABLE_COLUMNS[table_name].index(query_criteria["column"])], query_criteria["value"])
        return compare_dict[query_criteria["criteria"]](
            row[config.TABLE_COLUMNS[table_name].index(query_criteria["column"])], query_criteria["value"])


def granter_than(row_value, criteria_value):
    """
    比较列值是否大于查询值
    :param row_value: 列值
    :param criteria_value: 查询值 
    :return: 比较结果
    """
    if row_value > criteria_value:
        return True
    return False


def equals(row_value, criteria_value):
    """
    比较列值是否等于查询值
    :param row_value: 列值
    :param criteria_value: 查询值 
    :return: 比较结果
    """
    if row_value == criteria_value:
        return True
    return False


def like(row_value, criteria_value):
    """
    比较列值是否匹配查询值
    :param row_value: 列值
    :param criteria_value: 查询值 
    :return: 比较结果
    """
    if row_value.find(criteria_value) != -1:
        return True
    return False


def check_table_name(table_name):
    """
    验证表名是否存在
    :param table_name: 要验证的表名
    :return: 验证结果
    """
    if table_name in config.TABLE_NAMES:
        return True
    else:
        print("表名不存在")


def check_table_columns(table_name, table_columns):
    """
    验证列名是否存在
    :param table_name: 表名
    :param table_columns: 要验证的列名元组
    :return: 验证结果
    """
    if set(table_columns).issubset(config.TABLE_COLUMNS[table_name]):
        return True
    else:
        diff_set = set(table_columns).difference(config.TABLE_COLUMNS[table_name])
        print("列%s不存在" % ','.join(list(diff_set)))


def check_duplicate_columns(table_columns):
    """
    验证列名是否重复，查询不用验证，插入、更新需要验证
    :param table_columns: 列名元组
    :return: 验证结果
    """
    if len(set(table_columns)) == len(table_columns):
        return True
    else:
        print("列名重复")


def check_primary_key(table_name, row, columns_and_values):
    """
    验证主键
    :param table_name: 表名
    :param row: 数据库中的行数据字符串
    :param columns_and_values: 要写入数据库的行数据元组
    :return: 是否通过验证
    """
    # 要用strip()方法去除换行符
    if config.PRIMARY_KEY in config.TABLE_CONSTRAINTS[table_name]:
        row_index = config.TABLE_COLUMNS[table_name]. \
            index(config.TABLE_CONSTRAINTS[table_name][config.PRIMARY_KEY])
        if row[row_index] == columns_and_values[config.TABLE_CONSTRAINTS[table_name][config.PRIMARY_KEY]]:
            print("主键重复")
            return False
        if not columns_and_values[config.TABLE_CONSTRAINTS[table_name][config.PRIMARY_KEY]]:
            print("主键不能为空")
            return False
    return True


def check_auto_increment(table_name, row, columns_and_values):
    """
    验证自增列
    :param table_name: 表名
    :param row: 数据库中的行数据元组
    :param columns_and_values: 要写入数据库的列值字典
    :return: 目前自增列的最大值
    """
    max_value = 0
    if config.AUTO_INCREMENT in config.TABLE_CONSTRAINTS[table_name]:
        row_index = config.TABLE_COLUMNS[table_name]. \
            index(config.TABLE_CONSTRAINTS[table_name][config.AUTO_INCREMENT])
        if row[row_index] == columns_and_values[config.TABLE_CONSTRAINTS[table_name][config.AUTO_INCREMENT]]:
            print("自增列重复")
        else:
            max_value = row[row_index]
    return max_value


def check_data_valid(table_name, table_columns_and_values):
    """
    验证数据有效性
    :param table_name: 表名 
    :param table_columns_and_values: 列值字典
    :return: 验证结果
    """
    data_valid = True
    for key in table_columns_and_values:
        if config.TABEL_COLUMNS_TYPE[table_name][key] == int:
            if table_columns_and_values[key] and not table_columns_and_values[key].isdigit():
                print("列%s应为数字" % key)
                data_valid = False
                break
        if len(table_columns_and_values[key]) > config.TABLE_COLUMNS_LEN[table_name][key]:
            print("列%s值过大" % key)
            data_valid = False
            break
    return data_valid
