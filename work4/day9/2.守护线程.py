import time
import threading

def run(n):
    print('[%i]----------running----\n' % n)
    time.sleep(2)
    print('---done---')

def main():
    for i in range(5):
        t = threading.Thread(target = run,args = [i,])
        t.start()
        t.join()
        print('starting thread',t.getName())


m = threading.Thread(target=main,args=[])
m.setDaemon(True)#守护线程的作用是，当他结束后，子线程也自动被干掉
print('main thread',m.getName())
m.start()
m.join(timeout=5) #加锁不运行该线程了，然后5秒后结束该线程
print('---main thread done---')#不加join()会同时执行这个和start()后的子进程