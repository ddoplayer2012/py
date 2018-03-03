#_*_ coding:utf-8 _*_
import time
import threading
import random
from multiprocessing import Process,Queue,Pipe,Manager
import os
'''
SyncManager.register('Queue', Queue.Queue)
SyncManager.register('JoinableQueue', Queue.Queue)
SyncManager.register('Event', threading.Event, EventProxy)
SyncManager.register('Lock', threading.Lock, AcquirerProxy)
SyncManager.register('RLock', threading.RLock, AcquirerProxy)
SyncManager.register('Semaphore', threading.Semaphore, AcquirerProxy)
SyncManager.register('BoundedSemaphore', threading.BoundedSemaphore,
                     AcquirerProxy)
SyncManager.register('Condition', threading.Condition, ConditionProxy)
SyncManager.register('Pool', Pool, PoolProxy)
SyncManager.register('list', list, ListProxy)
SyncManager.register('dict', dict, DictProxy)
SyncManager.register('Value', Value, ValueProxy)
SyncManager.register('Array', Array, ArrayProxy)
SyncManager.register('Namespace', Namespace, NamespaceProxy)

# types returned by methods of PoolProxy
SyncManager.register('Iterator', proxytype=IteratorProxy, create_method=False)
SyncManager.register('AsyncResult', create_method=False)
'''

def f(d,l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.append(1)
    print(l)
#创建的进程连main函数里的列表和字典都不能共享访问。。。。但线程可以
# if __name__ == '__main__':
#     #创建一个管道的两端，父子连接
#     with Manager() as manager:
#         #d = manager.dict()
#         #l = manager.list(range(5))
#         d = {}  # 用普通的字典是无法在进程间共享的
#         l = []
#         p_list = []
#         for i in range(10):
#             p = Process(target=f,args=(d,l))
#             p.start()
#             p_list.append(p)
#         for res in p_list:
#             res.join()
#         print(d) #用manager字典，则会在进程间互相调用如果是普通字典d也为空
#         print(l)#l加了10个1在l的末尾，如果是普通字典，则l最后为空

#试一试线程玩一下,尽管结果和进程不同，但是还是能某种程度共享main函数，f函数内的运行结果不能共享，manager()的结果和进程是一样的
if __name__ == '__main__':
    #创建一个管道的两端，父子连接
    with Manager() as manager:
        #d = manager.dict()
        #l = manager.list(range(5))
        d = {}  # 用普通的字典是无法在进程间共享的
        l = []
        p_list = []
        for i in range(10):
            p = threading.Thread(target=f,args=(d,l))
            p.start()
            p_list.append(p)
        for res in p_list:
            res.join()
        print(d) #用manager字典，则会在进程间互相调用如果是普通字典d也为空
        print(l)#l加了10个1在l的末尾，如果是普通字典，则l最后为空