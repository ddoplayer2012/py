# -*- coding:utf-8 -*-

import socketserver

class MyServer(socketserver.BaseRequestHandler):    #$ 必须继承BaseRequestHandler
    def handle(self):        #$ 必须有handle方法
        print('New connection:',self.client_address)
        while True:
            data = self.request.recv(1024)
            if not data:break
            print('Client data:',data.decode())
            self.request.send(data)

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1',9999),MyServer)    #$ 实现多线程的socket
    server.serve_forever()    #$ 当前连接断开不会出现关闭或报错，可以与其他客户端继续连接