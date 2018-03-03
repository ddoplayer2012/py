#_*_ coding:utf-8 _*_
import time
import threading
import random
from multiprocessing import Process,Queue,Pipe,Manager
import os
'''
    #这里必须用multiprocessing的queue
import Queue 是没用的会报错
'''

def f(q):
    q.send(['hehe',None,'haha'])
    q.close()

if __name__ == '__main__':
    #创建一个管道的两端，父子连接
    parent_conn ,child_conn = Pipe()
    p = Process(target=f,args=(child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()
    Manager()