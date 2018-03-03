

def warraper(navi)  :
    print(navi)
    def cal_func(func):
        def add_args(*args,**kwargs):
            print("i'm caller")
            func(*args,**kwargs)
        return add_args
    return cal_func   #这里不返回，test2报错
@warraper(navi="hahahaha")
def test1():
    print("hehe,我是test1")

#如果这里不写navi,会报错
@warraper(navi="hehehehe")
def test2(name,age):
    print("hehe,我是%s,%d"%(name,age))

test1()
test2("ne",15)