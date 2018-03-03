笔记和博客
http://blog.51cto.com/13522822  day4 和day5开头的文章



使用方法：pycharm下设置atm_copy为source Root
运行atm_copy/bin/start.py 根据菜单选择操作
│  readme.txt
│ 
│
├─bin
│      start.py    运行总程序
│
├─config
│  │  configure.py    公用文件配置
│  │  __init__.py
│  │
│
├─db
│  ├─admin
│  │      alex           管理员信息
│  │      cardnum        开户卡号缓存
│  │
│  └─userinfo
│      ├─62220819060007  	  用户卡号
│      │  │  basic_info.json   用户信息数据
│
├─lib
│  │  hash.py     MD5加密
│  │
│  
│
└─src
    │  admin.py    管理员入口
    │  user.py     用户入口
    │
    ├─backend
    │  │  logger.py   日志模块




