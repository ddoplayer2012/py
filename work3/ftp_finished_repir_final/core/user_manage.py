#-*- coding:utf-8 -*-

import os,sys
import shelve
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
#print(sys.path)
from conf import configure as conf
from . import users
from . import user_clients as client
from lib import hash



class user_manage(object):
    '''
    用户类：
    1.用户添加
    2.用户修改
    3.用户空间增加
    4.查询空间
    '''
    def __init__(self):
        '''
         如果目录不存在，则创建数据库目录
         如果Admin账号文件不存在，则初始化admin账号，运行init_admin_user
        '''
        try:
            self.sock_flag = False
            self.name = ""
            if not os.path.exists(conf.admin_db_filepath):
                os.makedirs(conf.admin_db_filepath)
            if not os.path.exists(conf.users_db_filepath):
                os.makedirs(conf.users_db_filepath)
            admin_user = 'admin'
            admin_file_path = conf.admin_db_filepath + '\\' + admin_user
            if not os.path.exists(admin_file_path):
                os.makedirs(admin_file_path)
                if  not os.path.exists(admin_file_path + '\\' + '.dat'):
                    print('鉴于是第一次登录，初始化管理员账户为admin,123456')
                    user_home_path = conf.FTP_BASE + '\\' + admin_user
                    # 初始化ftp目录
                    if not os.path.exists(user_home_path):
                        os.makedirs(user_home_path)
                    self.init_admin_user(admin_file_path + '\\' + admin_user)

        except Exception as e:
            print(e)

    def init_admin_user(self,filepath):
        '''
        添加默认用户admin , 密码123456
        :param filepath:
        :return:
        '''
        try:
            self.admin_db = shelve.open(filepath,flag = "c", writeback = True)
            admin_obj = users.Users('admin',hash.hash('123456'))
            self.admin_db['admin']=admin_obj
        except Exception as e:
            print(e)

    def add_user(self,name,password):
        '''
        管理员新建其他用户
        :param name: 用户名
        :param password: 密码
        :return:
        '''
        try:
            print('当前权限'+self.user_obj.role)
            if self.user_obj.role == 'administrator':
                user_file_path = conf.users_db_filepath + '\\' + name
                if not os.path.exists(user_file_path):
                    os.makedirs(user_file_path)
                    user_file = user_file_path + '\\' + name
                    self.user_db = shelve.open(user_file,flag = "c", writeback = True)
                    password_encrypt = hash.hash(password)
                    user_obj = users.Users(name,password_encrypt)
                    #添加hash模块加密密码
                    self.user_db[name]=user_obj
                    user_home_path = conf.FTP_BASE + '\\' + name
                    #print(user_home_path)
                    if not os.path.exists(user_home_path):
                        os.makedirs(user_home_path)
                    if os.path.exists(user_file + '.dat') and os.path.exists(user_home_path):
                        print('添加用户%s成功' % name)
                    self.user_db.close()
                else:
                    print('该用户已存在，无法添加')
        except Exception as e:
            print(e)

    def login(self):
        '''
        登陆验证，成功后进入管理菜单
        :return:
        '''
        try:
            errcount = 1
            while errcount <= 3:
                name = input('请输入用户名：').strip()
                if name == 'admin' :
                    self.user_file_path = conf.admin_db_filepath + '\\' + 'admin'
                elif name == '':
                    print('用户名非法')
                    continue
                else:
                    self.user_file_path = conf.users_db_filepath + '\\' + name

                if  os.path.exists(self.user_file_path):

                    self.db_dict = shelve.open(self.user_file_path+ '\\' + name) #读取数据库获取用户信息
                    self.user_obj = self.db_dict[name]

                    user_name = self.user_obj.name
                    user_password = str(self.user_obj.password)
                    password = str(input('请输入密码：')).strip()
                    if user_name == name and user_password == hash.hash(password):
                        print("登录成功,进入管理界面")
                        self.name = user_name
                        self.password = user_password
                        self.user_home_path = conf.FTP_BASE + '\\' + user_name
                        if not os.path.exists(self.user_home_path):
                            print('用户FTP目录不存在,自动创建')
                            os.makedirs(self.user_home_path)
                        self.cur_path = self.user_home_path  # 初始化用户目录，路径
                        self.manage_view(user_name)
                    else:
                        print('用户名密码错误,次数' + str(errcount))
                        errcount += 1
                    self.db_dict.close()

                else:
                    print(self.user_file_path)
                    print('用户文件不存在')
                    break
        except Exception as e:
            print(e)


    def add_space(self):
        '''
        添加用户空间
        :return:
        '''
        try:
            print('当前权限' + self.user_obj.role)
            if self.user_obj.role == 'administrator':
                user_file_path = conf.users_db_filepath + '\\' + self.name
                if  os.path.exists(self.user_file_path):
                    #os.mkdir(self.user_file_path)
                    user_file = self.user_file_path + '\\' + self.name
                    self.user_db = shelve.open(user_file, flag="c", writeback=True)
                    spaces = int(input('请输入要增加的空间量(KB)：'))
                    self.user_obj.total_space += spaces
                    print('增加成功，当前总空间为：%s'% self.user_obj.total_space)
                    input('Press Enter to continue.....')
                    self.user_db[self.name] = self.user_obj
                    self.user_db.close()
                else:
                    print(user_file_path)
                    print('该用户不存在，无法添加')
            else:
                print('当前用户权限不足')
        except Exception as e:
            print(e)

    def get_user_info(self):
        '''
        打印用户信息
        :return:
        '''
        info = '''
            用户名：   %s
            可用空间： %s MB
            剩余空间： %s MB
            用户权限： %s
        '''%(self.user_obj.name,round(self.user_obj.total_space/1024/1024,2),round(self.user_obj.userd_space/1024/1024,2),self.user_obj.role)
        print(info)
        if self.user_obj.role == 'administrator':
            print('您是管理员，可以自由增改可用空间')
        input('Press Enter to continue.....')


    def ftp_help(self):
        '''
        打印帮助
        :return:
        '''
        help_msg = '''        help:
                                                            -----------ftp-----------------
                                                                 put   上传文件到当前目录
                                                                 get   下载
                                                                 ls    查看文件
                                                                 pwd   查看路径
                                                                 delete删除文件(不支持删除目录）
                                                                 cd    改变路径
                                                                 quit  注销登录
                                                                 exit  退出程序
                                                                 help  显示一次帮助
                                                                 mkdir 创建文件夹
                                                        '''
        print(help_msg)
    def manage_view(self,name):
        '''
        管理界面
        1.用户操作
        2.命令执行 ls mkdir rm put get等
        :param name:
        :return:
        '''
        try:
            if self.name == name:
                info = '''
                                      help:
                                      -----------ftp-----------------
                                           conn     连接ftp
                                      -----------用户管理-------------
                                           adduser  添加用户(需要管理员)
                                           info     获取当前用户信息
                                           addspace 增加ftp个人空间(需要管理员)
                                           hide     关闭菜单提示
                                           help     显示一次帮助
                                           exit     退出程序
                                  '''
                while self.sock_flag == False: #当标识为0,打印用户管理菜单
                    print(info)
                    cmd = input( name+' ~#')  #仿inux界面
                    menu = {
                            'addspace' : self.add_space
                            }
                    if menu.get(cmd):
                        menu[cmd]()
                    if cmd == 'adduser':
                        if self.user_obj.role == 'administrator':
                            add_user_name = input('输入增加用户的姓名：')
                            add_user_password = input('输入增加的用户密码：')
                            self.add_user(add_user_name,add_user_password)
                        else:
                            print('当前用户权限不足')
                    elif cmd == 'hide':
                        info = ''
                        print('隐藏菜单了，可以输入dis显示菜单')
                    elif cmd == 'help':
                        self.ftp_help()
                    elif cmd == 'conn':
                        self.sock = client.Myclient(conf.SERVER_IPPORT,name)
                        self.sock_flag = True
                        self.auth_rs = self.sock.start(["auth",self.name,self.password])
                        print('用户已经连接ftp，将失去用户管理功能')
                    elif cmd == 'info':
                        self.get_user_info()
                    elif cmd == 'exit':
                        exit('用户选择退出')
                    else:
                        print('无效的命令，请重试')
                while self.sock_flag and self.auth_rs: #socket连接进去
                    self.ftp_help()
                    cmd = input( 'FTP@' +name+' ~#')  #仿inux界面
                    menu = {'ls': self.sock.ls2,
                            'cd': self.sock.cd,
                            'pwd':self.sock.pwd,
                            'exit':self.sock.exit,
                            }

                    if len(cmd)>1:#特殊处理，避免空格出bug
                        if cmd == 'quit':
                            menu[cmd]()
                            self.sock_flag = False
                            break
                        elif cmd == 'exit':
                            exit('用户退出程序')
                        elif cmd.split()[0] == 'put':
                            if len(cmd.split())> 1:
                                self.sock.put(cmd.split()[1].strip())
                            else:
                                print('需要参数,例如put d:\\test.txt')
                        elif cmd.split()[0] == 'get':
                            if len(cmd.split()) > 1:
                                self.sock.get(cmd.split()[1].strip())
                            else:
                                print('需要参数,例如get readme.txt')
                        elif cmd.split()[0] == 'mkdir':
                            if len(cmd.split()) > 1:
                                self.sock.mkdir(cmd.split()[1].strip())
                            else:
                                print('需要参数,例如mkdir directoryname')
                        elif cmd.split()[0] == 'delete':
                            if len(cmd.split()) > 1:
                                self.sock.delete(cmd.split()[1].strip())
                            else:
                                print('需要参数,例如delete filename')
                        elif menu.get(cmd):
                            menu[cmd]()
                        else:
                            print('输入不合法')
            else:
                print('异常登录，请检查程序')
        except Exception as e:
            print(e)
        finally:
            if self.sock_flag == True:
                self.sock.sock.close()

def run():
    '''
    运行程序
    :return:
    '''
    u1 = user_manage()
    u1.login()

