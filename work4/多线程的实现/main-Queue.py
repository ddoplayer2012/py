#_*_ coding:utf-8 _*_
from multiprocessing import Manager

import socket,time,threading
socket.setdefaulttimeout(3) #减少扫描的总耗时
import queue
def single_port(q):
    '''
    输入ip,端口，判断端口是否被占用
    :param ip:
    :param port:
    :return:
    '''
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,)
        #data = q.get()
        print(q.get())
        #rs = sock.connect_ex(data)

        '''
        This is like connect(address), but returns an error code (the errno value)
        instead of raising an exception when an error occurs.'''
        # if rs == 0:
        #     lock.acquire()
        #     print('ip: %s , port %s is userd'%(x))
        #     lock.release()
    except Exception as e:
        #print(e)
        print('hehe')

def full_port(ip,q):
    '''
    扫描该ip下所有端口
    :param ip:
    :return:
    '''
    try:
        print('启动%s扫描' % ip)
        start_time = time.time()
        for i in range(0,65536):
            #print(i)
            q.put((ip,i))
        #print(i)
        print('扫描完成，耗时%s'%(time.time()-start_time))
    except Exception as e:
        print('扫描出错')


if __name__ == '__main__':
    lock = threading.Lock()
    q = queue.Queue()
    a = threading.Thread(target=full_port,args=['127.0.0.1',q])
    b = threading.Thread(target=single_port,args=[q,])
    a.start()
    b.start()
    a.join()
    b.join()