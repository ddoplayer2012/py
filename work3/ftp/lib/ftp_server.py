#_*_ coding:utf-8 _*_

import socketserver
import os,sys
from conf import configure as conf
import shelve
import json

class Myserver(socketserver.BaseRequestHandler):

    exit_flag = False
    #请勿乱初始化，会报错！！！！！参数不够，这里卡了我一个小时去写测试方法。
    # def __init__(self):
    #     self.SESSION_OK = False

    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024)  # 接收
                if self.data:#不加这个在断开链接的时候会再循环一次，可能会报错，打印"客户端信息:b{}"
                    print("客户端地址：", self.client_address)
                    print("客户端信息：", self.data)

                    cmd_dct = self.data.decode("utf-8") #str binary
                    cmd = json.loads(cmd_dct) #dictionary
                    action = cmd["action"]
                    if cmd.get('msg'):
                        msg = cmd['msg']
                    else:
                        print('无参数执行%s' % action)
                    rs = hasattr(self, action)
                    if rs:
                        func = getattr(self, action)#获取函数地址
                        if cmd.get("msg"):
                            func(msg)
                        else:
                            func()

            except ConnectionResetError as e:
                print(e)
                break

    def ftp_auth(self,msg):
        '''
        用户认证，成功发送消息成功，失败返回失败消息
        :param msg:
        :return:
        '''
        try:
            auth_res = False
            #认证数据读取
            if len(msg) == 3:
                msg_type = msg[0]
                username = msg[1]
                password = msg[2]
                if username :  #如果存在则读取用户信息
                    self.db_data = shelve.open(conf.DB_PATH + '\\' + username + username)
                    self.user_obj = self.db_data[username]
                    db_username = self.user_obj.name
                    db_password = self.user_obj.password

                    if username == db_username and password == db_password:
                        print('验证通过')
                        self.SESSION_OK =True
                        #初始化登录会话信息
                        self.login_user = username
                        self.cur_path = conf.FTP_BASE + '\\' + username
                        self.home_path = conf.FTP_BASE + '\\' + username
                    else:
                        auth_res = False
                else:
                    auth_res = False
            else:
                auth_res = False
            if auth_res:
                msg = "%s::成功认证" % msg_type
                print('用户%s通过了认证' % username)
                self.db_data.close()
            else:
                msg = "%s::认证失败" % msg_type
                self.db_data.close()
            self.db_data.close()
            self.request.send(msg)
        except Exception as e:
            print(e)

    def has_privilege(self,path):
        '''
        验证目录权限,不能超过Home目录
        :param path:
        :return:
        '''
        abs_path = os.path.abspath(path)
        if abs_path.startswith(self.home_path):
            return True
        else:
            return False

    def ls(self, *args):
        """服务器端，查看当前路径下目录文件"""
        current_path = os.path.join(self.cur_path)
        lst = os.listdir(current_path)
        msg_dct = {
            "list": lst
        }
        self.request.send(msg_dct.encode("utf-8"))

    def testConn(self,*args):
        print('收到')

HOST, PORT = "127.0.0.1",9999
server =socketserver.ThreadingTCPServer((HOST,PORT),Myserver)

server.serve_forever()