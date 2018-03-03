#_*_ coding:utf-8 _*_
import time
import threading
import random
import Queue
'''
 def task_done(self):
        """Indicate that a formerly enqueued task is complete.
            表明队列中的任务执行完成
        Used by Queue consumer threads.  For each get() used to fetch a task,
        a subsequent call to task_done() tells the queue that the processing
        on the task is complete.

        If a join() is currently blocking, it will resume when all items
        have been processed (meaning that a task_done() call was received
        for every item that had been put() into the queue).

        Raises a ValueError if called more times than there were items
        placed in the queue.
        """


    def join(self):
        """Blocks until all items in the Queue have been gotten and processed.
            阻塞直到所有队列成员被处理
        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer thread calls task_done()
        to indicate the item was retrieved and all work on it is complete.

        When the count of unfinished tasks drops to zero, join() unblocks.
        """

    def qsize(self):
        """Return the approximate size of the queue (not reliable!)."""
            返回估计的队列大小（不可靠）
    def empty(self):
        """Return True if the queue is empty, False otherwise (not reliable!)."""
            如果队列是空，返回真，否则假（不可靠）
    def full(self):
        """Return True if the queue is full, False otherwise (not reliable!)."""
            如果队列是满的，返回真，否则假（不可靠）
    def put(self, item, block=True, timeout=None):
        """Put an item into the queue.
        插入队列
        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until a free slot is available. If 'timeout' is
        a positive number, it blocks at most 'timeout' seconds and raises
        the Full exception if no free slot was available within that time.
        Otherwise ('block' is false), put an item on the queue if a free slot
        is immediately available, else raise the Full exception ('timeout'
        is ignored in that case).
        """
    def put_nowait(self, item):
        """非阻塞put

        Only enqueue the item if a free slot is immediately available.
        Otherwise raise the Full exception.
        """
        return self.put(item, False)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.
        读取队列
'''

def producer():
    count = 0
    for i in range(10):
        time.sleep(random.randrange(3))
        q.put('包子 %i'%count)
        print('包子 %i出来了'%count)
        count += 1

def consumer(n):
    count = 0
    while count < 20:
        time.sleep(random.randrange(4))
        if not q.empty():
            data = q.get()
            #print(data)
            print('%s 正在吃包子 %i'%(n,count))
        else:
            print('---no baozi anymore---')
        count += 1


q = Queue.Queue()
p1 = threading.Thread(target=producer,)
p1.start()

c1 = threading.Thread(target=consumer("b"))
c1.start()