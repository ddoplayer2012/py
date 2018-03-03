#-*- coding:utf-8 -*-
import time
import threading
'''
互斥锁Mutex
python2.7运行起来没毛病。。
总之在修改数据之前需要加锁，确保线程之间共享数据的安全性
'''
def addnum():
    global num
    print('--get num:',num)
    #time.sleep(1)
    lock.acquire()#加
    num -= 1
    lock.release()#解锁


num = 100
thread_list = []
lock = threading.Lock()  #共享锁
lock1 = threading.RLock() #递归锁，子锁。线程里的子线程也可以加锁
for i in range(100):

    t =threading.Thread(target=addnum())
    t.start()
    thread_list.append(t)

for t in thread_list:
     t.join()

print('final num:',num)