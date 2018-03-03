# -*- coding:utf-8 -*-
import os
import logging
import time
import json

from config import configure
from src.backend import logger
from lib import hash

CURRENT_USER_INFO = {}


def update_current_user_info():
    '''
    结账保存文件
    :return:
    '''
    json.dump(CURRENT_USER_INFO, open(os.path.join(configure.USER_DIR_FOLDER, str(CURRENT_USER_INFO['card']), "basic_info.json"), 'w'))


def write_logger(message):
    """
    写日志
    :param message:
    :return:
    """
    struct_time = time.localtime()
    logger_obj = logger.write_logger(CURRENT_USER_INFO['card'], struct_time)
    logger_obj.info(message)


def account_info():
    """
    账户信息
    :return:
    """
    cardname = (CURRENT_USER_INFO['card'])
    #print(cardname)
    user_dict = json.load(open(os.path.join(configure.USER_DIR_FOLDER, str(cardname), "basic_info.json"), 'r'))
    info = '''
       姓名: %s
       卡号: %s
       信用卡额度: %d 
       本月可用额度: %d
       储蓄金额: %d
       到期时间: %s
       状态: %s
       债务:%s
      ''' % (user_dict['username'], user_dict['card'], user_dict['credit'], user_dict['balance'], user_dict['saving'],
             user_dict['expire_date'], user_dict['status'], user_dict['debt'])
    print(info)
    input("按[回车]键继续")


def repay():
    """
    还款
    :return:
    """

    if CURRENT_USER_INFO['debt'] > 0:
        print("该账户欠款:" + str(CURRENT_USER_INFO['debt']))
        repaymoney = int(input("请输入还款金额>"))
        if repaymoney <= CURRENT_USER_INFO['debt']:
            if repaymoney > CURRENT_USER_INFO['saving']:
                print("储蓄金额不足,将使用信用卡还款")
                temp = repaymoney - CURRENT_USER_INFO['saving']
                if CURRENT_USER_INFO['balance'] > (temp + temp * 0.05):
                    CURRENT_USER_INFO['balance'] -= temp
                    CURRENT_USER_INFO['balance'] -= temp * 0.05
                    CURRENT_USER_INFO['debt'] -= repaymoney
                    write_logger('%s - 储蓄账户：%f；信用卡账户：%f；手续费：%f' % ("还款", CURRENT_USER_INFO['saving'], temp, temp * 0.05))
                    print("还款成功，现有债务剩余:"+ str(CURRENT_USER_INFO['debt']),"信用卡余额：" + str(CURRENT_USER_INFO['balance']))
                    update_current_user_info()
                else:
                    print('卡上余额不足，无法完成还款')

            else:
                CURRENT_USER_INFO['saving'] -= repaymoney
                CURRENT_USER_INFO['debt'] -= repaymoney
                write_logger('%s - 储蓄账户：%d' % ("还款", repaymoney))
                update_current_user_info()
        else:
            print("您是要送钱吗")
    else:
        print("debt:" + str(CURRENT_USER_INFO['debt']) + "不用还款")
def withdraw():
    """
    提现
    提现时，优先从自己余额中拿，如果余额不足，则使用信用卡（额度限制），提现需要手续费5%
    :return:
    """
    money = float(input('请输入提现金额'))
    if CURRENT_USER_INFO['saving'] >= money:
        CURRENT_USER_INFO['saving'] -= money
        write_logger('%s - 储蓄账户：%d' % ("提现", money))
        update_current_user_info()

    else:
        print('余额不足，正在从信用卡中提现')
        temp = money - CURRENT_USER_INFO['saving']
        if CURRENT_USER_INFO['balance'] > (temp + temp * 0.05):
            CURRENT_USER_INFO['balance'] -= temp
            CURRENT_USER_INFO['balance'] -= temp * 0.05

            write_logger('%s - 储蓄账户：%f；信用卡账户：%f；手续费：%f' % ("提现", CURRENT_USER_INFO['saving'], temp, temp * 0.05))
            update_current_user_info()
        else:
            print('信用卡余额:'+CURRENT_USER_INFO['balance']+'不足，无法完成提现')


def transfer():
    """
    转账
    :return:
    """
    cardname = str(input('请输入待转入的卡号：'))
    other_dict = json.load(open(os.path.join(configure.USER_DIR_FOLDER, cardname, "basic_info.json"), 'r'))
    if other_dict != None:
        money = int(input('请输入转入的资金：'))
        if CURRENT_USER_INFO['saving'] >= money:
            CURRENT_USER_INFO['saving'] -= money
            other_dict['saving'] += money
            write_logger('%s - 储蓄账户：%d 到 卡号-%s的储蓄账户 ' % ("转出", money,cardname))
            update_current_user_info()
            json.dump(other_dict,
                      open(os.path.join(configure.USER_DIR_FOLDER, cardname, "basic_info.json"),
                           'w'))
            print("转帐成功，储蓄卡余额：" + str(CURRENT_USER_INFO['saving']))

        else:
            print('余额不足，正在从信用卡中提现')
            temp = money - CURRENT_USER_INFO['saving']
            if CURRENT_USER_INFO['balance'] > (temp + temp * 0.05):
                CURRENT_USER_INFO['balance'] -= temp
                CURRENT_USER_INFO['balance'] -= temp * 0.05
                other_dict['saving'] += money
                write_logger('%s - 储蓄账户：%f；信用卡账户：%f；手续费：%f 到 卡号-%s的储蓄账户  ' % ("转出", CURRENT_USER_INFO['saving'], temp, temp * 0.05,cardname))
                update_current_user_info()
                json.dump(other_dict,
                          open(os.path.join(configure.USER_DIR_FOLDER, cardname, "basic_info.json"),
                               'w'))
                print("转帐成功，信用卡余额：" + str(CURRENT_USER_INFO['balance']))

            else:
                print('信用卡余额:' + CURRENT_USER_INFO['balance'] + '不足，无法完成转账')





def main():
    menu = '''
    1.  账户信息
    2.  还款
    3.  取款
    4.  转账

    '''
    menu_dic = {
        '1': account_info,
        '2': repay,
        '3': withdraw,
        '4': transfer,

    }
    while True:
        print(menu)
        user_option = input(">>:").strip()
        if user_option in menu_dic:
            menu_dic[user_option]()
        else:
            print("选项不存在")


def init(card):

    basic_info = json.load(open(os.path.join(configure.USER_DIR_FOLDER, str(card), "basic_info.json")))
    CURRENT_USER_INFO.update(basic_info)
    return (basic_info)

def login():
    """
    登陆
    :return:用户卡号信息
    """
    try:
        while True:
            card_num = input("请输入卡号:")
            userdict = init(card_num)
            if   userdict['status'] != 0:
                print("该帐号已被冻结")
                continue
            card_pass = input("请输入密码")
            if  str(userdict['card']) == str(card_num) and  userdict['password'] == hash.md5(card_pass):
                main()
                return userdict
            else:
                print("登录失败，卡号或密码错误")

    except Exception as e:
        if FileNotFoundError:
            print('卡号不存在')
        else:
            print(e)

def run():
    ret = login()
    if ret != None:
        print(ret)
        main()

