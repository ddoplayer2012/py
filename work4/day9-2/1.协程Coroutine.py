'''
1.协程是一种用户态的轻量级线程
2.协程有自己的register上下文和栈，协程调度切换时，将寄存器的上下文和栈保存到其他地方，在切回来的时候，回复先前保存的寄存器上下文和栈
因此：协程能保留上一次调用的状态（即所有局部状态的一个特定组合），每次过程重入时，就相当于进入上一次调用的状态，换种说法，进入上一次离开时所处逻辑流的位置
advantage:
1.无需线程上下文切换的开销
2.无需atomic operation锁定及同步的开销
atomic operation原子操作一旦开始，就一直运行到结束，中间不会有任何切换到另外线程的操作，原子操作可以是一个或多个步骤，但是顺序不会被打乱
3.方便切换控制流，简化变成模型
4.高并发+高扩展+低成本：一个cpu可以支持上万个协程

disadvantage:
1.无法利用多核资源
2.进行阻塞blocking操作如（IO)时会阻塞掉整个程序

协程的直接条件：
1.必须在一个单线程里实现并发
2.修改共享数据不需要加锁
3.用户程序里自己保存多个控制流的上下文栈
4.一个协程遇到IO操作自动切换到其他协程
'''
#greenlet ,gevent是第三方库的协程
import gevent
#2.继承式调用

