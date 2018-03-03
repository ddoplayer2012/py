# -*- coding:utf-8 -*-
import logging
from config import configure
import os
import time


def write_logger(card_num, struct_time):
    if struct_time.tm_mday < 25:
        filename = "%s_%s_%d" % (struct_time.tm_year, struct_time.tm_mon, 24)
    else:
        # 下个月
        filename = "%s_%s_d" % (struct_time.tm_year, struct_time.tm_mon + 1, 24)
    #file_handler2 = logging.FileHandler(
    #    os.path.join(configure.USER_DIR_FOLDER, str(card_num), "record", filename), encoding='utf-8')

    # fmt = logging.Formatter(fmt="%(asctime)s :  %(message)s")
    # file_handler2.setFormatter(fmt)
    #
    # logger1 = logging.Logger('user_logger', level=logging.INFO)
    # logger1.addHandler(file_handler2)
    # return logger1
    file_handler2 = logging.FileHandler(
        os.path.join(configure.USER_DIR_FOLDER, str(card_num), "record", filename), encoding='utf-8')
    #fmt = logging.Formatter(fmt="(asctime)s:%(message)s")
    #不知为何这么写就不出日期格式
    fmt = logging.Formatter(fmt="%(asctime)s :  %(message)s")
    file_handler2.setFormatter(fmt)
    logger1 = logging.Logger('user_logger', level=logging.INFO)
    logger1.addHandler(file_handler2)
    return logger1