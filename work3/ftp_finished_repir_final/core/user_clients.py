#-*- coding:utf-8 -*-
import socket
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import json
import hashlib


def cat_exception(origin_func):
    '''
    该装饰器并没有使用
    :param origin_func:
    :return:
    '''
    def warpper(*args,**kwargs):
        try:
            if self.auth_result:
                u = origin_func(self,*args,**kwargs)
                return u
            else:
                exit('没有ftp认证，程序退出，请重新连接')
        except Exception as e:
            return 'an exception raised...'
    return warpper()

class Myclient(object):
    #客户端类

    def __init__(self,ip_port,name):
        '''
        初始化客户端
        :param ip_port: 元祖形式，（IP，port)
        :param name: 用户名
        '''
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
        try:
            self.sock.connect((self.ip_port))
        except Exception as e:
            print(e)
    def auth(self,message):
        '''
        认证方法
        1.成功，返回True，用于后续方法的入口验证
        2.失败，返回False,同上，如果False,后面的方法都无法正常运行
        :param message: ["auth",self.name,self.password] 这是一个传送用户名和密码的参数
        :return:
        '''
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
        '''
        启动客户端程序
        1.调用connect方法，建立socket连接到服务器
        2.auth认证方法，发送认证信息到服务器
        :param message:["auth",self.name,self.password] 这是一个传送用户名和密码的参数
        :return:返回
        '''
        self.auth_result = False
        #开始,认证用户，保存用户登录信息和目录信息到
        self.connect()
        print('欢迎%s使用ftp'%self.name)
        #print(message)
        self.auth_result = self.auth(message)
        if self.auth_result:
             return  True
    def cd(self):
        '''
        change directory
        使用方法和传统的有略微不同。这个是输出cd回车后，再输入目录
        1.进入方法后，先发送一个参数进行验证，返回可切换的目录
        2.获取用户输入，切换
        :return: BOOL
        '''
        try:
            if self.auth_result:
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
            else:
                print("用户未连接ftp认证，无权使用cd")
                return
        except Exception as e:
            print(e)
    def pwd(self):
        '''
        显示当前路径
        :return:
        '''
        try:
            if self.auth_result:
                #显示当前路径
                self.cmd_send('ls')
                # 接收文件状态，是否改变成功
                server_response = self.sock.recv(1024)
                if server_response:
                    server_dct = self.loads_msg(server_response)
                    cur_dir = server_dct['list']['root']
                    print('当前目录%s' % cur_dir)
            else:
                print("用户未连接ftp认证，无权使用pwd")
                return
        except Exception as e:
            print(e)

    def put(self, *args):
        '''
        1.验证认证信息
        2.判断本地文件路径是否存在，发送握手信息
        3.判断磁盘配额
        4.判断文件状态{正常上传，已存在同名需要重命名，需要续传}
        5.如果是续传，改变文件的指针到续传点
        6.开始上传
        7.生成md5,发送md5
        8.获取返回md5，判断传输结果
        :param args: 文件名
        :return:
        '''
        try:
            if self.auth_result:
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
                            if  server_response['breakout'] is not None:
                                print('存在文件断点%s，正在续传...' % server_response['breakout'])
                                # 接着发送文件内容
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
                        if  server_response['breakout'] is not None:
                            f.seek(break_size, 0)
                            print(f.tell())
                        for line in f:
                            self.sock.send(line)
                            #m.update(line)#
                            send_len += len(line)
                            #经过测试，进度条在pycharm里不会显示，在控制台里显示良好。
                            percent = int(round(send_len/size, 2)*100)
                            progress_mark = "=" * int(percent / 2)
                            print("[%s/%s]%s>%s" % (size, send_len, progress_mark, percent),end= '\r')
                            sys.stdout.flush()
                            if send_len >= size:
                                print('文件读取完毕')
                        f.close()
                        f = open(file_fullname, "rb")
                        m.update(f.read())#
                        # 可以增加MD5校验
                        self.sock.send(m.hexdigest().encode("utf-8"))
                        res = self.sock.recv(1024).decode("utf-8")
                        if res =="0" and  server_response['status'] == "OK":
                            print("文件传输成功，剩余空间%s" % server_response['size'])
                        elif server_response['status'] == "rename":
                            print("文件传输成功,重命名为new_%s" % msg_dct['filename'])
                        elif  res =="0" and  server_response['status'] == "continue":
                            print("文件续传成功，剩余空间%s" % server_response['size'])

                        else:
                            print("文件传输失败")
                    else:
                        print("文件不存在 %s" % file_fullname)
            else:
                print('用户未认证ftp,无权使用put')
                return
        except Exception as e:
            print(e)

    def get(self,*args):
        '''
        1.发送握手信息
        2.获取返回信息{文件存在[继续下载]，文件不存在[退出]}
        3.返回信息正确，进行下载步骤
        4.下载完成校验MD5
        5.发送MD5，获取比对信息
        6.比对信息正确，下载成功，否则下载失败
        :param args: 文件名
        :return:
        '''
        try:
            if self.auth_result:
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
                                print("文件下载出错")
                                msg = self.format_msg("get::failed")
                                self.sock.send(msg)
                else:
                    print('get参数不正确')
            else:
                print('用户未连接ftp认证,无权使用get')
                return
        except Exception as e:
            print(e)

    def mkdir(self,*args):
        '''
        创建目录
        1.获取目录信息
        2.发送目录命令
        3.获取目录创建结果
        :param args:
        :return:
        '''
        try:
            if self.auth_result:
                cmd_split = args[0].split(" ")
                if len(cmd_split) > 0:#参数正确则继续
                    dirname = cmd_split[0]
                    msg_dct = {
                        "dirname": dirname
                    }
                    #发送
                    self.cmd_send('mkdir',msg_dct)
                    data = self.sock.recv(1024)  # 接收文件
                    decode_data = self.loads_msg(data)
                    rec_cmd = decode_data.split("::")[0]
                    rec_result = decode_data.split('::')[1]
                    if rec_cmd == 'mkdir' and rec_result =='success':
                        print('目录创建成功')
                    elif rec_cmd == 'mkdir' and rec_result =='failed':
                        print('目录创建失败，服务器权限不足')
                    else:
                        print('程序异常，请联系管理员')
            else:
                print("用户未连接ftp认证，无权使用pwd")
                return
        except Exception as e:
            print(e)
    def delete(self,*args):
        '''
        1.发送握手信息
        2.获取返回信息，命令在服务端处理
        3.根据返回信息打印结果
        :param args:
        :return:
        '''
        try:
            if self.auth_result:
                cmd_split = args[0].split(" ")
                if len(cmd_split) > 0:#参数正确则继续
                    filename = cmd_split[0]
                    msg_dct = {
                        "filename": filename
                    }
                    #发送
                    self.cmd_send('delete',msg_dct)
                    data = self.sock.recv(1024)  # 接收文件
                    decode_data = self.loads_msg(data)
                    rec_cmd = decode_data.split("::")[0]
                    rec_result = decode_data.split('::')[1]
                    if rec_cmd == 'delete' and rec_result =='success':
                        print('删除成功')
                    elif rec_cmd == 'delete' and rec_result =='failed':
                        print('删除失败，服务器权限不足')
                    elif rec_cmd == 'delete' and rec_result == 'not file':
                        print('删除失败，目前只支持删除文件')
                    else:
                        print('程序异常，请联系管理员')
            else:
                print("用户未连接ftp认证，无权使用pwd")
                return
        except Exception as e:
            print(e)
    def testConn(self):
        #测试连接，前期使用
        msg_dct = {
            "action": "testConn"
        }
        cmdstr = json.dumps(msg_dct)
        self.sock.send(cmdstr.encode("utf-8"))
        print('???')

    def ls2(self, *args):
        '''
        1.发送命令ls
        2.获取返回结果信息
        3.判断结果，打印输出
        :param args:
        :return:
        '''
        try:
            if self.auth_result:
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
            else:
                print('用户未连接ftp认证,无权使用ls')
                return
        except Exception as e:
            print(e)
    def format_msg(self,msg):
        '''
        发送字符串前格式化成json二进制
        :param msg:
        :return:
        '''
        return  json.dumps(msg).encode("utf-8")
    def loads_msg(self,msg):
        '''
        解码json二进制为字符串
        :param msg:
        :return:
        '''
        return json.loads(msg.decode("utf-8"))

    def cmd_send(self,command,msg=None):
        '''
        包装起来的socket.send，包含json二进制封装
        :param command: ls
        :param msg: 函数内定义好的消息
        :return:
        '''
        try:
            if self.auth_result:
                msg_dct = {
                    "action": command,
                    "msg": msg
                }
                # 第一次发送操作文件信息
                msg = self.format_msg(msg_dct)
                self.sock.send(msg)
        except Exception as e:
            print(e)
    def exit(self):
        #退出
        self.auth_result = False
        self.sock.close()

# ip_port = ("127.0.0.1",9999)
# c = Myclient(ip_port,'admin')
# #c.start()
# c.start(["auth","admin","123456"])
# x = '-l'.encode("utf-8")
# c.testConn()
# c.sock.close()
