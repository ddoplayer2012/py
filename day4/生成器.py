__author__ = "Alex Li"

import time
def consumer(name):
    print("%s顾客来啦"%name)
    while True:
        mantou= yield
        print("第%s个馒头被%s吃了"%(mantou,name))



def producer(name):
    c= consumer("金角")
    c2=consumer("银角")
    c3 = consumer("葫芦")
    c.__next__()
    c2.__next__()
    c3.__next__()
    print("老子开始准备做包子啦!")
    for i in range(10):
        time.sleep(1)
        print("做了1个包子,分3半!")
        c.send(i)
        c2.send(i)
        c3.send(i)

producer("alex")