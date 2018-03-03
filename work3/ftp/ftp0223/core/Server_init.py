#-*- coding:utf-8 -*-

import os
import shelve
from conf import configure as conf
from lib import ftp_server as ser



server = ser.socketserver.ThreadingTCPServer(conf.PORT,ser.Myserver)
print('启动ftp服务...')
server.serve_forever()