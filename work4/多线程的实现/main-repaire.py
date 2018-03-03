#_*_ coding:utf-8 _*_
import socket,time,threading
socket.setdefaulttimeout(2) #减少扫描的总耗时


class scanner(threading.Thread):
    q = [] #队列存储
    maxthreads = 100#线程并发
    event = threading.Event()
    lock = threading.Lock()

    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        try:
            pass
        except Exception as e:
            print(e.message)
    #完成的线程弄出队列
        scanner.lock.acquire()
        scanner.q.remove(self)
        #如果移除后队列数==99，则说明有线程正在等待，释放event，让等待事件执行
        if len(scanner.q) == scanner.maxthreads - 1:
            scanner.event.set()
            scanner.event.clear()
        scanner.lock.release()


def run_scan(ip,port):
    for i in range(1,100):
        scanner.lock.acquire()
        #如果超过队列上限则等待
        if len(scanner.q) > scanner.maxthreads:
            scanner.lock.release()
            scanner.event.wait() #遇到set则结束等待
        else:
            scanner.lock.release()

        scanner.newthread(ip,port)
    for t in scanner.q:
        t.join()
def test(h):
    print('test%s'%h)
def single_port(ip,port):
    '''
    输入ip,端口，判断端口是否被占用
    :param ip:
    :param port:
    :return:
    '''

    if port >= 65535:
        print(u'程序异常')
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,)
    rs = sock.connect_ex((ip,port))
    '''
    This is like connect(address), but returns an error code (the errno value)
    instead of raising an exception when an error occurs.'''
    if rs == 0:
        scanner.lock.acquire()
        print('ip: %s , port %s is userd'%(ip,port))
        scanner.lock.release()

def newthread(ip):
    scanner.lock.acquire()
    for i in range(10):
        sc = scanner(target=single_port,args=[ip,i,])
        scanner.q.append(sc)
        scanner.lock.release()
        sc.start()


newthread('127.0.0.1')