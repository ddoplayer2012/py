#_*_ coding:utf-8 _*_

import socket,time,threading
socket.setdefaulttimeout(3) #减少扫描的总耗时

def single_port(ip,port):
    '''
    输入ip,端口，判断端口是否被占用
    :param ip:
    :param port:
    :return:
    '''
    try:
        if port >= 65535:
            print(u'程序异常')
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,)
        rs = sock.connect_ex((ip,port))
        '''
        This is like connect(address), but returns an error code (the errno value)
        instead of raising an exception when an error occurs.'''
        if rs == 0:
            lock.acquire()
            print('ip: %s , port %s is userd'%(ip,port))
            lock.release()
    except Exception as e:
        #print(e)
        print('hehe')

def full_port(ip):
    '''
    扫描该ip下所有端口
    :param ip:
    :return:
    '''
    try:
        print('启动%s扫描' % ip)
        start_time = time.time()
        for i in range(0,65534):
            threading._start_new_thread(single_port,(ip,i))

        print('扫描完成，耗时%s'%(time.time()-start_time))

    except Exception as e:
        print('扫描出错')
        #print(e)

if __name__ == '__main__':
    x = input('输入扫描信息:')
    lock = threading.Lock()
    full_port(x)
