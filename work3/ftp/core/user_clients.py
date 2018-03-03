#-*- coding:utf-8 -*-
import socket
import os,sys
from conf import configure as conf
import json
class Myclient(object):
    #客户端类

    def __init__(self,ip_port,name):
        self.func_dict = {
            'help': 'help',
            'get': 'get',
            'put': 'put',
            'exit': 'exit',
            'ls': 'ls',
            'cd': 'cd',
            'del': 'del'
        }
        #定义socket的信息，但是不连接。。。要验证登录再连接
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ip_port = ip_port
        self.exit_flag = False
        self.name = name
        # if self.auth():
        #     self.interactive()

    def connect(self):
        #连接
        self.sock.connect((self.ip_port))
    def auth(self):
        #认证
        msg_dct = {
            "action": "ftp_auth"
        }
        msg_dct["msg"] = ["auth", "admin", "123456"]
        # 第一次发送操作文件信息
        msg = self.format_msg(msg_dct)
        self.sock.send(msg)
    def start(self):
        #开始,认证用户，保存用户登录信息和目录信息到
        self.connect()
        print('欢迎%s使用ftp'%self.name)
        #self.auth()
        # while True:
        #     self.interactive()
    def interactive(self):
        #开始交互
        ftp_cmd = input('FTPSERVER~%s #'%self.name)
        info = '''
                                                            help:
                                                            -----------ftp-----------------
                                                                 put   上传文件到当前目录
                                                                 get   下载
                                                                 ls    查看文件
                                                                 pwd   查看路径
                                                                 del   删除文件
                                                                 cd    改变路径
                                                                 exit  退出程序
                                                                 help  显示一次帮助
                                                        '''
        print(info)


    def put_file(self,msg):
        #上传
        if len(msg) == 2:
            if os.path.isfile(msg[1]):
                file_size = os.path.getsize(msg[1])
                instruction_msg = "file_tansfer|put|sendready|%s|%s" % (msg[1],file_size)
                self.sock.send(instruction_msg)
                feedback = self.sock.recv(1024)
                print('==>',feedback)
                progress_percent = 0
                if feedback.startswith("file_tansfer::put_file::recv_ready"):
                    f = open(msg[1],"rb")
                    sent_size = 0
                    while not sent_size == file_size:
                        if file_size - sent_size <=1024:
                            data = f.read(file_size - sent_size)
                            sent_size += file_size - sent_size
                        else:
                            data = f.read(1024)
                            sent_size += 1024
                        self.sock.sebd(data)

                        cur_percent = int(float(sent_size) / file_size * 100)
                        if cur_percent > progress_percent:
                            progress_percent = cur_percent
                            self.show_progress(file_size,sent_size,progress_percent)
                    else:
                        print('--文件:%s 传输完毕--' % msg[1])
                    f.close()

            else:
                print('File %s 不在磁盘上' % msg[1])
    def show_progress(self,total,finished,percent):
        #用sys.stdout.write方法实现
        progress_mark = "=" * (percent / 2)
        sys.stdout.write("[%s/%s]%s>%s\r" % (total,finished,progress_mark,percent))
        sys.stdout.flush()
        if percent == 100:
            print('\n')
    def testConn(self):
        msg_dct = {
            "action": "testConn"
        }
        cmdstr = json.dumps(msg_dct)
        self.sock.send(cmdstr.encode("utf-8"))
        print('???')
        # # 接收文件状态，是否改变成功
        # server_response = self.sock.recv(1024)
        # server_dct = server_response.decode("utf-8")
        #
        # print(server_dct["list"])
    def ls2(self, *args):
        """客户端，查看文件目录"""
        msg_dct = {
            "action": "ls"
        }
        # 第一次发送操作文件信息
        msg = self.format_msg(msg_dct)
        self.sock.send(msg)

        # 接收文件状态，是否改变成功
        server_response = self.sock.recv(1024)
        if server_response:
            server_dct = json.loads(server_response.decode("utf-8"))
            print(server_dct["list"])
    def format_msg(self,msg):
        return  json.dumps(msg).encode("utf-8")
ip_port = ("127.0.0.1",9999)
c = Myclient(ip_port,'admin')
c.start()
#c.start(["auth","admin","123456"])
x = '-l'.encode("utf-8")
c.testConn()
c.sock.close()
