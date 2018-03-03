#-*- coding:utf-8 -*-
'''
启动ftp server

'''
import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)



from conf import configure as conf
from lib import ftp_server as ser

server = ser.socketserver.ThreadingTCPServer(conf.SERVER_IPPORT,ser.Myserver)
print('启动ftp服务...')
server.serve_forever()


