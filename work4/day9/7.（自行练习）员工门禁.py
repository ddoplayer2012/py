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

def door():

    open_count = 0
    while True:
        if  door_event.isSet():
            print('门是开着的')
            open_count += 1
        else:
            print('门是关着的，正准备刷卡开门')
            open_count = 0
            door_event.wait()
        if open_count > 3:
            print('门开了3秒了，该关了%s'%open_count)
            door_event.clear()
        time.sleep(0.5)

def men(n):
    print('[%s] is coming' % n)
    while True:
        if door_event.is_set():
            print('[%s] door is opened,passing' % n)
            break
        else:
            print('[%s] 看见门是关的，掏出门禁卡开门'% n)
            print(door_event.set())
            door_event.set()
            print('after',door_event.set())
        time.sleep(0.5)


door_event = threading.Event()
door_thread = threading.Thread(target=door)
door_thread.start()

for i in range(5):
    x = threading.Thread(target=men,args=[i,])
    time.sleep(random.randrange(3))
    x.start()