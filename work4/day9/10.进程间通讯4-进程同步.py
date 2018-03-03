#_*_ coding:utf-8 _*_
import time
import threading
import random
from multiprocessing import Process,Queue,Pipe,Manager,Lock
import os
'''
不使用锁，来混合各进程的资源,这种操作---6666
'''

def f(l,i):
    l.acquire()
    try:
        print('hello world', i)
    except Exception as e:
        print(e)
    finally:#无论如何释放锁
        l.release()

if __name__ == '__main__':
    lock = Lock()
    for num in range(10):
        Process(target=f,args=(lock,num)).start()