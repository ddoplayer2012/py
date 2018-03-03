#-*- coding:utf-8 -*-
import socket
import os,sys
from conf import configure as conf
import json
import hashlib
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
    def auth(self,message):
        #认证
        msg_dct = {
            "action": "ftp_auth"
        }
        #msg_dct["msg"] = ["auth", "admin", "123456"]
        msg_dct["msg"] = message
        # 第一次发送操作文件信息
        send_msg = self.format_msg(msg_dct)
        self.sock.send(send_msg)
        server_response = self.sock.recv(1024)
        server_dct = server_response.decode("utf-8")
        response_list = json.loads(server_dct)
        msg_type = response_list.split('::')[0]
        msg_result = response_list.split('::')[1]
        if msg_type == 'auth' and msg_result == 'success':
            return True
        elif msg_type == 'auth' and msg_result == 'failed':
            print('认证失败%s' % msg_result)
            return False
        else:
            print('接受信息错误！请联系管理员')

    def start(self,message):
        self.auth_result = False
        #开始,认证用户，保存用户登录信息和目录信息到
        self.connect()
        print('欢迎%s使用ftp'%self.name)
        #print(message)
        self.auth_result = self.auth(message)
        while self.auth_result:
             return  True
    def cd(self):
        self.cmd_send('ls')
        # 接收文件状态，是否改变成功
        server_response = self.sock.recv(1024)
        if server_response:
            server_dct = self.loads_msg(server_response)
            cur_dir = server_dct['list']['root']
            while True:
                print('当前目录%s' % cur_dir)
                selected_path = input('请输入切换的目录名')
                if selected_path == 'q' or selected_path == 'Q':
                    return False
                if selected_path in server_dct['list']['dirs'] or selected_path == '~' or selected_path == '..':
                    self.cmd_send("cd", "cd::" + selected_path)
                    server_response = self.sock.recv(1024)
                    if server_response:
                        server_dct = self.loads_msg(server_response)
                        server_dct = server_dct.split('::')
                        if server_dct[1] == 'success' and server_dct[0] == 'cd':
                            print('切换目录成功')
                            return True
                else:
                    print('无效的路径，请重试')
    def pwd(self):
        #显示当前路径
        self.cmd_send('ls')
        # 接收文件状态，是否改变成功
        server_response = self.sock.recv(1024)
        if server_response:
            server_dct = self.loads_msg(server_response)
            cur_dir = server_dct['list']['root']
            print('当前目录%s' % cur_dir)

    def put(self, *args):
        """客户端，发送文件，已测试可以单个文件上传"""
        cmd_split = args[0].split(" ")
        if len(cmd_split)>0:
            file_fullname = cmd_split[0]
            # 判断文件是否存在，存在则继续
            if os.path.isfile(file_fullname):
                size = os.stat(file_fullname).st_size  # 获取文件大小
                msg_dct = {
                    "filename": os.path.basename(file_fullname),
                    "size": size,
                    "override": True
                }
                send_len = 0
                # 第一次发送操作文件信息
                self.cmd_send('put',msg_dct)
                # 确认接收，防止粘包，确认服务器空间是否足够
                server_response = self.sock.recv(1024)
                server_response = self.loads_msg(server_response)
                if server_response['status'] == "continue" :
                    print("空间足够")
                    if server_response['breakout']:
                        print('存在文件断点%s，正在续传...' % server_response['breakout'])
                        # 接着发送文件内容
                        m = hashlib.md5()
                        break_size = server_response['breakout']
                        send_len = break_size
                elif server_response['status'] == "OK" :
                    pass
                elif server_response['status'] == "rename":
                    print('检测到重名文件，自动重新命名')
                else:
                    print("空间不足")
                    return  # 中断操作

                # 接着发送文件内容
                m = hashlib.md5()
                f = open(file_fullname, "rb")
                if server_response['breakout']:
                    f.seek(break_size, 0)
                    print(f.tell())
                for line in f:
                    self.sock.send(line)
                    m.update(line)
                    send_len += len(line)
                    #经过测试，进度条在pycharm里不会显示，在控制台里显示良好。
                    percent = int(round(send_len/size, 2)*100)
                    progress_mark = "=" * int(percent / 2)
                    print("[%s/%s]%s>%s" % (size, send_len, progress_mark, percent),end= '\r')
                    sys.stdout.flush()
                    if send_len >= size:
                        print('文件读取完毕')
                f.close()

                # 可以增加MD5校验
                self.sock.send(m.hexdigest().encode("utf-8"))
                res = self.sock.recv(1024).decode("utf-8")
                if res =="0" and  server_response['status'] == "OK":
                    print("文件传输成功，剩余空间%s"%server_response['size'])
                elif server_response['status'] == "rename":
                    print("文件传输成功,重命名为new_%s" % msg_dct['filename'])
                else:
                    print("文件传输失败")
            else:
                print("文件不存在 %s" % file_fullname)
    def get(self,*args):
        #客户端请求下载
        try:
            cmd_split = args[0].split(" ")
            if len(cmd_split) > 0:#参数正确则继续
                file_name = cmd_split[0]
                msg_dct = {
                    "filename": file_name,
                    "LocalPath": "D:\\"
                }
                # 第一次发送操作文件信息
                self.cmd_send('get', msg_dct)#发送get请求握手
                res = self.sock.recv(1024)
                decode_res = self.loads_msg(res)
                decode_res_cmd = decode_res.split("::")[0]
                decode_res_result = decode_res.split("::")[1]
                decode_res_filesize = int(decode_res.split("::")[2])#文件大小
                if decode_res_cmd == 'get' and decode_res_result == 'READY':
                    #握手确认文件存在，下一步进入传输阶段
                    file_fullname = os.path.join(msg_dct['LocalPath'],file_name)
                    f = open(file_fullname, "wb")
                    received_size = 0
                    m = hashlib.md5()
                    while received_size < decode_res_filesize:
                        if decode_res_filesize - received_size > 1024:
                            size = 1024
                        else:
                            size =  decode_res_filesize - received_size
                        data = self.sock.recv(size)#接收文件
                        f.write(data)
                        m.update(data)
                        received_size += len(data)
                    else:
                        f.close()
                        received_md5 = self.sock.recv(1024).decode("utf-8")#接收文件校验
                        if m.hexdigest() == received_md5:
                            if os.path.isfile(file_fullname):
                                print("文件下载成功%s" %(file_fullname))
                                msg = self.format_msg("get::success")
                                self.sock.send(msg)
                        else:
                            print("文件上传出错")
                            msg = self.format_msg("get::failed")
                            self.sock.send(msg)
            else:
                print('get参数不正确')
        except Exception as e:
            print(e)


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
        self.cmd_send('ls')
        # 接收文件状态，是否改变成功
        server_response = self.sock.recv(1024)
        if server_response:
            server_dct = self.loads_msg(server_response)
            cur_dir = server_dct['list']['root']
            print('当前目录%s' % cur_dir)
            for key in server_dct['list']['dirs']:
                print('d---------\t%s' % key)
            for key in server_dct['list']['files']:
                print('f---------\t%s' % key)
    def format_msg(self,msg):
        return  json.dumps(msg).encode("utf-8")
    def loads_msg(self,msg):
        return json.loads(msg.decode("utf-8"))

    def cmd_send(self,command,msg=None):
        if self.auth_result:
            msg_dct = {
                "action": command,
                "msg": msg
            }
            # 第一次发送操作文件信息
            msg = self.format_msg(msg_dct)
            self.sock.send(msg)
    def exit(self):
        #退出
        self.auth_result = False
        self.sock.close()
# ip_port = ("127.0.0.1",9999)
# c = Myclient(ip_port,'admin')
# #c.start()
# c.start(["auth","admin","123456"])
# x = '-l'.encode("utf-8")
# c.auth()
# c.sock.close()
