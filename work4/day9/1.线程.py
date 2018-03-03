import threading
import time

#1.直接调用
# def sayhi(num):
#
#         print('运行的数字%s'%num)
#         time.sleep(3)
#
#
# if __name__ == '__main__':
#     t1 = threading.Thread(target = sayhi ,args=(1,))
#     t2 = threading.Thread(target = sayhi,args=(1,))
#
#     t1.start()
#     t2.start()
#
#     print(t1.getName())
#     print(t2.getName())

#2.继承式调用

class MyThread(threading.Thread):
    def __init__(self,num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        print('运行的数字%s'% self.num)
        time.sleep(3)

if __name__ == '__main__':
    t1 = MyThread(2)
    t2 = MyThread(3)

    t1.start()
    t2.start()
