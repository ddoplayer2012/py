# -*- coding:utf-8 -*-
import socket
import json
ip_port = ('127.0.0.1', 9999)
sk = socket.socket()
sk.connect(ip_port)
msg_dct = {
    "action": "testConn"
}
cmdstr = json.dumps(msg_dct).encode("utf-8")
sk.send(cmdstr)
#sk.sendall(('请求占领地球'.encode('utf-8')))
server_reply = sk.recv(1024).decode("utf-8")
print(server_reply)

sk.close()

