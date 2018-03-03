笔记：blog.51cto.com/13522822 下面day8的就是
## 要求：

1. 用户加密认证(md5密码加密)
2. 允许同时多用户登录(多用户认证接口)
3. 每个用户有自己的家目录 ，且只能访问自己的家目录(创建用户时候自动设置)
4. 对用户进行磁盘配额，每个用户的可用空间不同(lib\ftpserver里上传put实现判断此项)
5. 允许用户在ftp server上随意切换目录(cd)
6. 允许用户查看前目录下文件（ls)
7. 允许上传和下载文件，保证文件一致性（hash验证保持文件一致）
8. 文件传输过程中显示进度条（控制台下可以流畅显示，pycharm里能够显示（文件需要够大）-刷新率很低。）
9. 附加功能：支持文件的断点续传（已写入put程序，get没写）

错误1：I_NET4 必须是元祖，而非列表报错。。。。ip,port必须整合成元祖形式才能发布端口
错误2：import的时候会运行一遍被调用的程序！！！！！会运行一遍被调用的程序！！！！！！会运行一遍被调用的！！！！！！！程序。
不知道为何会这样Server_init.py  文件内容,不知道为何会调用到client去了:解决方法，把client.py换个名字。。。。治标不治本，跑了一次后又出现这种情况

错误3:初始化子类没有观察父类的初始化条件，并且忘记了这里有个初始化，调试的时候断点没设置对甚至都找不到在哪初始化报错。。
class Myserver(socketserver.BaseRequestHandler):
    exit_flag = False
    #请勿乱初始化，会报错！！！！！参数不够，写测试方法的时候发现的，调试的时候看不到，但有了这次经验以后会注意到的。
    # def __init__(self):
    #     self.SESSION_OK = False

警告1：进度条在pycharm里不会显示的很流畅，在控制台可以显示，但是目前还是不会如何打包py项目。先在Pycharm里实现基本的功能先
警告2：断点续传：逻辑编写出错导致续传不合理，在经过大量测试和调试后解决
    后续解决和避免方案
    1.调试出错则检查逻辑
    2.变量命名尽量简单明了，大量变量经过计算后不直接用于逻辑判断，先设置一个变量名来存储，方便后期阅读和修改！


使用步骤：0.运行bin下的start.py   startclient.py
          1.登录  默认管理员admin 123456 ,或者删除/db文件夹重新初始化
          2.用户管理，按照菜单来做
          3.如果再用户管理里选择连接ftp,连接后按照命令使用方法来操作
       	  4.断点续传测试方法：传输一个20mb左右的文件，传输到一半，结束程序，然后再次运行startclient.py,可发现续传成功

命令使用方法
put   d:\op.txt    上传文件
get   op.txt       下载文件，默认d:\
ls    查看文件     无需参数
pwd   查看路径     无需参数
delete op.txt      删除文件
cd    hh           改变路径
exit  退出程序
help  显示一次帮助
mkdir hh           创建文件夹

ftp目录
├─.idea
│  └─inspectionProfiles
├─bin   start.py   运行ftpserver程序
├   startclient.py  运行client
├─conf  configure.py  配置信息文件
├─core
│user_clients.py 客户端程序，由user_manage调用
│user_manage.py  主程序，整合用户管理和ftp连接
│users.py        用户类，定义数据存储结构
├─db    数据库文件，存放用户信息
│  ├─admin
│  │  └─admin
│  └─uesrs
├─ftpfiles  ftp文件，存放上传文件
│  └─admin
│      ├─ha
│      └─hh
├─lib
│ ftp_server.py ftp服务端
│ hash.py       加密md5
└─test         测试程序

用户数据库结构user.py
```
{
    "name":name,
    "password":password,
    "total_size":size,
    "used_size":size,
}
```

流程图：见压缩包内流程图文件夹


