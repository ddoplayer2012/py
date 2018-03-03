#_*_ coding:utf-8 _*_
import time
import threading
import random
from multiprocessing import Process,Queue,Pipe,Manager,Lock,Pool
import os

'''
进程池内部维护一个序列，使用时去进程池里获取一个进程，如果没有可用的进程，则会阻塞直到有可用进程为止
进程池内部有两个方法 
apply           同步，必须有子进程响应
apply_async     异步，只管执行就行了
terminate       立即关闭进程池

'''

def Foo(i):
    time.sleep(2)
    return i* 100

def Bar(arg):
    print('--exec done:',arg)
if __name__ == '__main__':
    pool= Pool(5)
    for i in range(10):
        pool.apply_async(func=Foo,args=(i,),callback=Bar)
        #pool.apply(func=Foo,args=(i,))
    print('end')
    pool.close()
    pool.join()#注释掉后，程序直接结束了，否则程序会等待子进程运行完毕后关闭
    #while True:
    #    pass