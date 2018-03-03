#_*_ coding:utf-8 _*_

import socketserver
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from conf import configure as conf
import shelve
import json
from lib import hash
import hashlib
class Myserver(socketserver.BaseRequestHandler):

    exit_flag = False
    #请勿乱初始化，会报错！！！！！参数不够，这里卡了我一个小时去写测试方法。

    def handle(self):
        '''
        继承后需要重写这个方法，处理socket信息
        :return:
        '''
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
        1.处理msg提取信息
        2.打开数据库比对用户信息
        3.返回验证结果发送回客户端
        :param msg: 客户端定义的msg格式
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
                    if username == 'admin':
                        DB_PATH = conf.admin_db_filepath
                    else:
                        DB_PATH = conf.users_db_filepath
                    self.db_data = shelve.open(DB_PATH + '\\' + username + '\\' + username)
                    self.user_obj = self.db_data[username]
                    self.db_username = self.user_obj.name
                    db_password = self.user_obj.password

                    if username == self.db_username and (password) == db_password:
                        print('验证通过')
                        auth_res =True
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
                msg = "%s::success" % msg_type
                print('用户%s通过了认证' % username)
                self.db_data.close()
            else:
                msg = "%s::failed" % msg_type
                self.db_data.close()
            self.db_data.close()
            send_msg = self.format_msg(msg)
            self.request.send(send_msg)
        except Exception as e:
            print(e)

    def has_privilege(self,path):
        '''
        验证目录权限,不能超过Home目录
        '''
        abs_path = os.path.abspath(path)
        if abs_path.startswith(self.home_path):
            return True
        else:
            return False

    def put(self,msg):
        '''
        处理Put方法
        1.验证用户磁盘配额
        2.处理msg
        3.生成验证结果字典，发送回客户端
        4.验证通过，开始发送文件
        :param msg:
        :return:
        '''
        try:
            """服务器端，接收文件"""
            #打开数据库，读取用户配额
            m = hashlib.md5() #初始化加密
            if self.db_username == 'admin':
                DB_PATH = conf.admin_db_filepath
            else:
                DB_PATH = conf.users_db_filepath
            self.db_data = shelve.open(DB_PATH + '\\' + self.db_username + '\\' + self.db_username,flag="c",writeback=True)
            self.user_obj = self.db_data[self.db_username]

            #初始化上传的文件信息
            cmd_dct= msg
            file_fullname = os.path.join(self.cur_path, cmd_dct["filename"])
            filesize = cmd_dct["size"]

            msg_dict = {
                'size': 0,    #剩余空间大小
                'breakout':None, #是否是续传，是则发送续传的byte数
                'status':'1',     #启动接收状态
                'tmp_filename':None
            }
            # 验证用户空间是否足够 确认接收,先假装空间够，后期再添加此功能
            pre_space = int(self.user_obj.userd_space) + int(filesize)
            total_space = int(self.user_obj.total_space)
            if  total_space > pre_space:
                msg_dict['size'] = pre_space
            else:
                msg_dict['status'] = "NO SPACE"
                self.request.send(self.format_msg(msg_dict))
                return
            # 接收文件内容,如果有断点则进行断点。。。目前没找到如何合理的触发文件中断传输，强行关闭程序一定会报错出BUG，无法断点继续，已在小文件上进行了理论测试，此等方案用seek偏移到下一个字节是可行的
            if os.path.isfile(file_fullname+'.tmp'):#存在文件断点
                received_size = os.stat(file_fullname+'.tmp').st_size
                msg_dict['breakout'] = received_size
                msg_dict['status'] = 'continue'
                msg_dict['tmp_filename'] = file_fullname+'.tmp'
                if received_size >= 0:
                    f = open(file_fullname + '.tmp', "ab")
                    f.seek(filesize,0)
                    print(f.tell())
                    self.request.send(self.format_msg(msg_dict))
                else:
                    print('文件传输ERROR大小错误')
                    msg_dict['status'] = ''
                    self.request.send(self.format_msg(msg_dict))
            else:
                received_size = 0
                if os.path.isfile(file_fullname):
                    file_fullname = os.path.join(self.cur_path,"new_" + cmd_dct["filename"])
                    f = open(file_fullname + '.tmp', "wb")
                    msg_dict['status'] = 'rename'
                    self.request.send(self.format_msg(msg_dict))
                else:
                    f = open(file_fullname + '.tmp', "wb")
                    msg_dict['status'] = 'OK'
                    self.request.send(self.format_msg(msg_dict))
            #循环接收文件块，每块1024byte
            while received_size < filesize:
                # 精确控制接收数据大小
                if filesize - received_size > 1024:
                    size = 1024
                else:
                    size = filesize - received_size
                data = self.request.recv(size)
                f.write(data)
                #m.update(data)#提升效率的验证方法，断点续传用不了
                received_size += len(data)
            else:#当最后一块
                f.close()
                #验证文件md5
                if os.stat(file_fullname+'.tmp').st_size > 0:
                    f = open(file_fullname+'.tmp', "rb")
                    # f.seek(0, 0)
                    m.update(f.read())
                    f.close()
                # 增加已经使用的空间
                self.user_obj.userd_space += int(filesize)
                #self.db_data.update(self.db_data[self.db_username])
                self.db_data.close()
                # MD5值校验
                received_md5 = self.request.recv(2048).decode("utf-8")
                local_md5 = m.hexdigest()
                if local_md5 == received_md5:
                    os.rename(file_fullname+'.tmp',file_fullname)
                    if os.path.isfile(file_fullname):
                        print("文件上传成功%s" % self.dir_replace(file_fullname))
                        self.request.send("0".encode("utf-8"))
                else:
                    print("文件上传出错")
                    #断电续传
                    self.request.send("-1".encode("utf-8"))
        except Exception as e:
            print(e)

    def get(self,msg):
        '''
        get方法，客户端下载文件
        1.处理msg,判断文件是否存在
        2.返回握手信息
        3.开始传输
        4.发送校验信息
        5.收取返回校验结果
        :param msg:
        :return:
        '''
        try:
            file_full_name = os.path.join(self.cur_path,msg['filename'])
            if os.path.isfile(file_full_name):#服务端存在该文件
                filesize = os.stat(file_full_name).st_size
                self.request.send(self.format_msg("get::READY::%s"%filesize))#握手信息
                # 接着发送文件内容
                m = hashlib.md5()
                send_len = 0
                f = open(file_full_name, "rb")
                for line in f:
                    self.request.send(line)
                    m.update(line)
                    send_len += len(line)
                f.close()
                # 可以增加MD5校验
                self.request.send(m.hexdigest().encode("utf-8"))#发送校验信息
                res = self.request.recv(1024).decode("utf-8")#收到校验返回信息
                if res == "get::success":
                    print("文件%s传输成功" % msg['filename'])
                else:
                    print("文件传输失败" % res)

            else:
                self.request.send(self.format_msg("get::NOT FOUND"))
        except Exception as e:
            print(e)

    def ls(self, *args):
        '''
        1.处理msg获取目录
        2.运行os.walk模拟LS，windows下操作
        3.返回ls的结果
        :param args:
        :return:
        '''
        lst = {}
        current_path = os.path.join(self.cur_path)
        for root,dirs,files in  os.walk(current_path) :
            lst['dirs'] = dirs
            lst['files'] = files
            lst['root'] = self.dir_replace(root)
            break
        #lst = os.listdir('current_path')  #方法二，直接列出文件和文件夹的列表，不够只管
        msg_dct = {
            "list": lst
        }
        msg_send = self.format_msg(msg_dct)
        self.request.send(msg_send)

    # def show_progress(self, total, finished, percent):
    #     # 用sys.stdout.write方法实现、
    #     progress_mark = "=" * int(percent * 100 )
    #     sys.stdout.write("[%s/%s]%s>%s\r" % (total, finished, progress_mark, percent))
    #     sys.stdout.flush()
    #     if percent == 100:
    #         print('\n')

    def mkdir(self,msg):
        '''
        创建目录
        1.处理msg,获取目录
        2.验证创建结果，返回客户端创建信息
        :param msg:
        :return:
        '''
        try:
            dirname = msg['dirname']
            dir_fullname = os.path.join(self.cur_path , dirname)
            os.mkdir(dir_fullname)
            if os.path.exists(dir_fullname):
                self.request.send(self.format_msg('mkdir::success'))
            else:
                self.request.send(self.format_msg('mkdir::failed'))
        except Exception as e:
            print(e)
    def delete(self,msg):
        '''
        仅支持删除文件
        1.处理msg,获取文件路径
        2.执行delete操作
        3.验证和返回操作结果
        :param msg:
        :return:
        '''
        try:
            filename = msg['filename']
            file_fullname = os.path.join(self.cur_path, filename)
            if not os.path.isdir(file_fullname):#非目录删除
                #删除操作
                os.remove(file_fullname)
                if not os.path.exists(file_fullname):
                    self.request.send(self.format_msg('delete::success'))
                else:
                    self.request.send(self.format_msg('delete::failed'))
            else:#目录回答不支持的操作
                self.request.send(self.format_msg('delete::not file'))

        except Exception as e:
            print(e)
    def cd(self,msg):
        '''
        1.处理msg,获取路径
        2.临时切换目录
        3.返回切换结果
        :param msg:
        :return:
        '''
        x = msg.split('::')
        if x[0] == 'cd':
            if x[1] == '..':
                self.cur_path = os.path.dirname(self.cur_path)
                msg = "cd::success"
                self.request.send(self.format_msg(msg))
            elif x[1] == '~':
                self.cur_path = self.home_path
                msg = "cd::success"
                self.request.send(self.format_msg(msg))
            else:
                temp_path = os.path.join(self.cur_path,x[1])
                if os.path.isdir(temp_path):
                    if self.has_privilege(temp_path):
                        self.cur_path = temp_path
                        msg = "cd::success"
                        self.request.send(self.format_msg(msg))
                    else:
                        msg = "cd::DIR OUT OF RANGE"
                        self.request.send(self.format_msg(msg))
                else:
                    msg = "cd::dir not exist"
                    self.request.send(self.format_msg(msg))
        else:
            msg = "cd::ERROR,CMD NOT FOUND"
            self.request.send(self.format_msg(msg))
    def testConn(self,*args):
        print('收到')
    def loads_msg(self,msg):
        #格式化二进制json为字符串
        return json.loads(msg.decode("utf-8"))
    def dir_replace(self, dir_path):
        #返回相对家目录路径
        return (dir_path.replace(self.home_path,self.db_username))
    def format_msg(self,msg):
        #格式化socket发送信息为binary字典
        return  json.dumps(msg).encode("utf-8")
# HOST, PORT = "127.0.0.1",9999
# server =socketserver.ThreadingTCPServer((HOST,PORT),Myserver)
# server.serve_forever()