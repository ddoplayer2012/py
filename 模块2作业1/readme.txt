1. 课程笔记
1.1 Python学习笔记九：装饰器，生成器，迭代器
http://www.cnblogs.com/koctr/p/7473895.html
1.2 Python学习笔记十：json序列化，软件结构目录规范，ATM作业讲解，import本质论
http://www.cnblogs.com/koctr/p/7473914.html
1.3 Python学习笔记十一：模块
http://www.cnblogs.com/koctr/p/7473932.html

2. 流程图
见流程图.zip

3. 作业说明
3.1 运行方法
运行bin目录下的staff.py，按照sql语法进行select、insert、update、delete，值用双引号引起来，表名为staff，相关配置信息
见conf目录下的config.py
例：
select * from staff
select * from staff where id=1
select name,age from staff where name like "Alex"
insert into staff values("", "Koctr Li", 33, 15112099999,"HR", "2000-07-01")
insert into staff values(10, "Liyong",40,18548135523,"HR","1999-09-01")
insert into staff (name,phone) values("Koch", 15210263666)
UPDATE staff SET dept="Market" where dept = "IT"
delete staff where dept="Market"

3.2 程序结构
|   readme.txt 项目readme
|   
+---.idea
|   |   misc.xml
|   |   modules.xml
|   |   Staff_info_manage.iml
|   |   workspace.xml
|   |   
|   \---inspectionProfiles
|           profiles_settings.xml
|           
+---bin
|       staff.py   程序入口
|       __init__.py
|       
+---conf
|   |   config.py        配置文件，包含数据字典
|   |   __init__.py
|   |   
|   \---__pycache__
|           config.cpython-36.pyc
|           __init__.cpython-36.pyc
|           
+---core
|   |   check.py         验证文件，用于验证各种条件，如：完整性约束、表名、列名是否存在
|   |   create.py        实现insert功能
|   |   db_handler.py    实现数据库连接
|   |   formatter.py     对输入的列、值、条件进行格式化
|   |   main.py          程序主文件
|   |   remove.py        实现delete功能
|   |   replace.py       实现update功能
|   |   search.py        实现select功能
|   |   __init__.py
|   |   
|   \---__pycache__
|           check.cpython-36.pyc
|           create.cpython-36.pyc
|           db_handler.cpython-36.pyc
|           formatter.cpython-36.pyc
|           main.cpython-36.pyc
|           remove.cpython-36.pyc
|           replace.cpython-36.pyc
|           search.cpython-36.pyc
|           __init__.cpython-36.pyc
|           
+---db
|   |   __init__.py
|   |   
|   \---staff
|           staff.bak
|           staff.db       数据库文件
|           __init__.py
|           
\---logs
        __init__.py

4. 问题集
见2017年10月16日新加内容
http://www.cnblogs.com/koctr/p/7257561.html
