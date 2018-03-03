#-*- coding:utf-8 -*-
import time
import threading
'''
semaphore 信号量，互斥锁只允许一个线程更改，semapyhore允许一定数量线程更改
总之在修改数据之前需要加锁，确保线程之间共享数据的安全性
'''
def run(n):
    semaphore.acquire()
    time.sleep(1)
    print('run the thread: %s \n' % n)
    semaphore.release()

if __name__ == '__main__':
    num = 0
    semaphore = threading.BoundedSemaphore(5)#5个线程同时运行
    for i in range(20):
        t = threading.Thread(target=run,args=[i,])
        t.start()
while threading.active_count() != 1:
    pass
else:
    print('----all threads done---')
    print(num)