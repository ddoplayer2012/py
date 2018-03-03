#-*- coding:utf-8 -*-
import time
import threading
import random
'''
event = threading.Event()
event.wait() 客户端等待事件被Set
event.set() 不做任何事
event.clear() 当flag是clear,阻塞直到set
'''

def light():
    if not event.isSet():
        event.set()
    count = 0
    while True:
        if count < 10:
            print('绿灯行')
        elif count< 13:
            print('黄灯警')
        elif count < 20:
            if event.isSet():
                event.clear()
            print('红灯停')
        else:
            count = 0
            event.set()
        time.sleep(1)
        count += 1

def car(n):
    while 1:
        time.sleep(random.randrange(10))
        if event.isSet():
            print('car [%s] is running..' % n)
        else:
            print('car [%s] is waiting for the red light..' % n)

if __name__ == '__main__':
    event = threading.Event()
    light = threading.Thread(target=light)
    light.start()
    for i in range(3):
        t = threading.Thread(target=car ,args= (i,))
        t.start()