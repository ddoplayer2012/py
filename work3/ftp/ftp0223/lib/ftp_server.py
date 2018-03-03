#_*_ coding:utf-8 _*_

import socketserver
import os,sys
from conf import configure as conf
import shelve
import json
from lib import hash
import hashlib
class Myserver(socketserver.BaseRequestHandler):

    exit_flag = False
    #请勿乱初始化，会报错！！！！！参数不够，这里卡了我一个小时去写测试方法。

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
        try:
            """服务器端，接收文件"""
            #打开数据库，读取用户配额
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

            if int(self.user_obj.total_space) < int(self.user_obj.userd_space) + int(msg_dict['size']):
                msg_dict['size'] = int(self.user_obj.userd_space) + int(filesize)
            else:
                msg_dict['status'] = "NO SPACE"

            # 接收文件内容,如果有断点则进行断点。。。目前没找到如何合理的触发文件中断传输，强行关闭程序一定会报错出BUG，无法断点继续，已在小文件上进行了理论测试，此等方案用seek偏移到下一个字节是可行的
            if os.path.isfile(file_fullname+'.tmp'):#存在文件断点
                filesize = os.stat(file_fullname+'.tmp').st_size
                msg_dict['breakout'] = filesize
                msg_dict['status'] = 'continue'
                msg_dict['tmp_filename'] = file_fullname+'.tmp'
                f = open(file_fullname + '.tmp', "wb")
                f.seek(filesize)
                print(f.tell())
                self.request.send(self.format_msg(msg_dict))
            else:
                if os.path.isfile(file_fullname):
                    file_fullname = os.path.join(self.cur_path,"new_" + cmd_dct["filename"])
                    f = open(file_fullname + '.tmp', "wb")
                    msg_dict['status'] = 'rename'
                    self.request.send(self.format_msg(msg_dict))
                else:
                    f = open(file_fullname + '.tmp', "wb")
                    msg_dict['status'] = 'OK'
                    self.request.send(self.format_msg(msg_dict))
            received_size = 0
            m = hashlib.md5()
            #循环接收文件块，每块1024byte
            while received_size < filesize:
                # 精确控制接收数据大小
                if filesize - received_size > 1024:
                    size = 1024
                else:
                    size = filesize - received_size
                data = self.request.recv(size)
                f.write(data)
                m.update(data)
                received_size += len(data)

            else:#当最后一块
                f.close()
                # 增加已经使用的空间
                self.user_obj.userd_space += int(filesize)
                #self.db_data.update(self.db_data[self.db_username])
                self.db_data.close()
                # MD5值校验
                received_md5 = self.request.recv(1024).decode("utf-8")
                if m.hexdigest() == received_md5:
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
        #给客户端发送消息
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
        """服务器端，查看当前路径下目录文件"""
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

    def show_progress(self, total, finished, percent):
        # 用sys.stdout.write方法实现、
        progress_mark = "=" * int(percent * 100 )
        sys.stdout.write("[%s/%s]%s>%s\r" % (total, finished, progress_mark, percent))
        sys.stdout.flush()
        if percent == 100:
            print('\n')


    def cd(self,msg):
        #切换目录cd
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
        return json.loads(msg.decode("utf-8"))
    def dir_replace(self, dir_path):
        #返回相对家目录路径
        return (dir_path.replace(self.home_path,self.db_username))
    def format_msg(self,msg):
        #格式化socket发送信息为binary字典
        return  json.dumps(msg).encode("utf-8")
HOST, PORT = "127.0.0.1",9999
server =socketserver.ThreadingTCPServer((HOST,PORT),Myserver)
server.serve_forever()