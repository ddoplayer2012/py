#_*_ coding:utf-8 _*_
import time
import threading
import random
import Queue
from multiprocessing import Process
import os
'''
multiprocessing使用像threading模块的API方式产生进程
可以用进程代替线程干掉GIL锁
'''

def info(title):
    print(title)
    print('module name:',__name__)
    print('parent process:',os.getppid())
    print('process id:',os.getpid())
    print('\n\n')
def info1(title):
    print(title)
    print('module name:',__name__)
    #print('parent process:',os.getppid())
    print('process id:',os.getpid())
    print('\n\n')
def f(name):
    info('function f')
    print('hello',name)


if __name__ == '__main__':
    info1('main process')

    p = Process(target=f,args=('haha',))
    p.start()
    p.join()