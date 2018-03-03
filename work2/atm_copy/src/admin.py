import os
import json
from lib import hash
from config import configure


global CURRENT_USER_INFO
CURRENT_USER_INFO = {'is_authenticated': False, 'current_user': None}



def init():
    """
    写入管理员
    :return:
    """
    dic = {'username': 'alex', 'password': hash.md5('123456')}
    json.dump(dic, open(os.path.join(configure.ADMIN_DIR_FOLDER, dic['username']), 'w'))

def main():
    try:
        print(CURRENT_USER_INFO)#
        if  CURRENT_USER_INFO['current_user'] == 'alex' and CURRENT_USER_INFO['is_authenticated'] == True:
            menu = """
            1、创建账户；
            2、删除账户；
            3、冻结账户；
            4、查询账户
            """
            menu_dic = {
                '1': create_user,
                '2': remove_user,
                '3': locked_user,
                '4': search,
            }
            while True:
                print(menu)
                user_option = input(">>:").strip()
                if user_option in menu_dic:
                    menu_dic[user_option]()
                else:
                    print("选项不存在")
        else:
            print('非法登录')
    except Exception as e:
        if FileNotFoundError:
            print('卡号或用户名不存在')
        else:
            print(e)



def create_user():
    """
    创建账户
    :return:
    """
    with open(os.path.join(configure.ADMIN_DIR_FOLDER,"cardnum"),'r')  as s:
        base_num = s.readline()
    username = input("输入要建立的用户名:")
    card_num = int(base_num) + 1
    with open(os.path.join(configure.ADMIN_DIR_FOLDER,"cardnum"),'w+')  as s:
        s.write(str(card_num))
    os.makedirs(os.path.join(configure.USER_DIR_FOLDER, str(card_num), 'record'))
    base_info = {'username': username,
                 'card': card_num,
                 'password': hash.md5('8888'),
                 "credit": 15000,  # 信用卡额度
                 "balance": 15000, # 本月可用额度
                 "saving": 0,      # 储蓄金额
                 "enroll_date": "2016-01-01",
                 'expire_date': '2021-01-01',
                 'status': 0,  # 0 = normal, 1 = locked, 2 = disabled
                 "debt": 500, # 欠款记录，如：[{'date': "2015_4_10", "total_debt":80000, "balance_debt": 5000},{'date': "2015_5_10", "total":80000, "balance": 5000} ]
                 }
    json.dump(base_info, open(os.path.join(configure.USER_DIR_FOLDER, str(card_num), "basic_info.json"), 'w'))
    print("已经新建了用户")

def remove_user():
    """
    移除账户
    :return:
    """
    cardname = input("请输入需要移除的卡号:")
    __import__('shutil').rmtree(os.path.join(configure.USER_DIR_FOLDER,cardname))

def locked_user():
    """
    冻结账户  'status': 0,  # 0 = normal, 1 = locked, 2 = disabled
    :return:
    """
    cardname = input("请输入冻结的卡号:")
    user_dict = json.load(open(os.path.join(configure.USER_DIR_FOLDER,cardname,"basic_info.json"), 'r'))
    #print(user_dict)
    user_dict['status'] = 1
    json.dump(user_dict, open(os.path.join(configure.USER_DIR_FOLDER, cardname, "basic_info.json"), 'w'))
    print('已冻结:'+ cardname)

def search():
    """
    搜索账户
    :return:
    """
    cardname = input("请输入查询的卡号:")
    user_dict = json.load(open(os.path.join(configure.USER_DIR_FOLDER, cardname, "basic_info.json"), 'r'))
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

def auth(auth_type):
    print("登录类型:",auth_type)
    def outer_wrapper(func):
        def wrapper(*args, **kwargs):
            global CURRENT_USER_INFO
            if auth_type == "web":
                username = input("Username:").strip()
                password = input("Password:").strip()
                user_dict = json.load(open(os.path.join(configure.ADMIN_DIR_FOLDER, username), 'r'))
                if username == user_dict['username'] and hash.md5(password) == user_dict['password']:
                    print("\033[32;1mUser has passed authentication\033[0m")
                    CURRENT_USER_INFO = {'is_authenticated': True, 'current_user': username}
                    res = func(*args, **kwargs)  # from home
                    return res
                else:
                    exit("\033[31;1mInvalid username or password\033[0m")

        return wrapper
    return outer_wrapper

def login():
    while True:
        global CURRENT_USER_INFO
        username = input("请输入管理员用户名：")
        password = input("请输入密码：")
        if not os.path.exists((os.path.join(configure.ADMIN_DIR_FOLDER,username))):
            print('用户名不存在')
        else:

            user_dict = json.load(open(os.path.join(configure.ADMIN_DIR_FOLDER, username), 'r'))
            if username == user_dict['username'] and hash.md5(password) == user_dict['password']:
                print('login')
                CURRENT_USER_INFO = {'is_authenticated':True , 'current_user': username}

                return True
            else:
                print('密码错误')

@auth(auth_type='web')
def auth_check():
    if CURRENT_USER_INFO['is_authenticated']:
        main()
    else:
        print("非法登录，发送邮件到管理员邮箱")
