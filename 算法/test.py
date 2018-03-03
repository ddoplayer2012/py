class Foo:

    def get_bar(self):
        return 'wupeiqi'

    # *必须两个参数
    def set_bar(self, value):
        return  'set value' + value

    def del_bar(self):
        return 'wupeiqi'

    BAR = property(get_bar, set_bar, del_bar, 'description...')

obj = Foo()


print(obj.BAR)              # 自动调用第一个参数中定义的方法：get_bar
obj.BAR = "alex"     # 自动调用第二个参数中定义的方法：set_bar方法，并将“alex”当作参数传入
#del Foo.BAR          # 自动调用第三个参数中定义的方法：del_bar方法
obj.BAR.__doc__      # 自动获取第四个参数中设置的值：description...
