#_*_ coding:utf-8 _*_
import time
import threading
import random
from multiprocessing import Process,Queue
import os
'''
    #这里必须用multiprocessing的queue
import Queue 是没用的会报错
'''

def f(q):
    q.put(['hehe',None,'haha'])


if __name__ == '__main__':
    #这里必须用multiprocessing的queue
    q =Queue()
    p = Process(target=f,args=(q,))
    p.start()
    print(q.get())
    p.join()