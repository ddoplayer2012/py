# -*- coding:utf-8 -*-
import socket
import json
ip_port = ('127.0.0.1', 9999)
sk = socket.socket()
sk.bind(ip_port)
sk.listen(5)

while True:
    print('server waiting ...')
    conn, addr = sk.accept()
    client_data = conn.recv(1024)
    str = json.loads(client_data.decode("utf-8"))
    print(str)
    conn.sendall('不要回答'.encode("utf-8"))
    conn.close()

