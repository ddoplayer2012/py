# -*- encoding:utf-8 -*-
# Author: Koctr


def file_db_handle(conn_params):
    """
    解析数据库文件路径(parse the db file path)
    :type conn_params: dict
    :param conn_params: 连接参数，参数在config.py文件中配置（conn_params: the db connection params set in settings）
    :return:
    """
    db_path = '%s/%s' % (conn_params['path'], conn_params['name'])
    return db_path


def db_handler(conn_params):
    """
    连接到数据库（connect to db）
    :type conn_params: dict
    :param conn_params: 连接参数，参数在config.py文件中配置（the db connection params set in settings）
    :return:a
    """
    if conn_params['engine'] == 'file_storage':
        return file_db_handle(conn_params)
    elif conn_params['engine'] == 'mysql':
        pass
