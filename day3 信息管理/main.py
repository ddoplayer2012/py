#获取文件
# -*- coding:utf-8 -*-
def get_info():
    userinfo = {}
    with open("info.txt","r",encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        line = line.split(" ")
       #print(line[0])
        if not(line[0] == ''):
            userinfo[line[0]] =line[1]
        else:
            pass
            #print("读取到空行")
    return userinfo

#更新用户工资
def update_info(username,salary):
    _userinfo = get_info()
    with open("info.txt","r",encoding="utf-8") as f:
        lines = f.readlines()
        linenum = 0
        #print(lines)
        if username  in _userinfo:
            str = username + "工资：" + _userinfo[username]
            print(str)
            for line in lines:
                if username in line:
                    _user_update = username + " " + salary
                    lines[linenum] = _user_update +"\n"
                    with open("info.txt", "w", encoding="utf-8") as fw:
                        fw.writelines(lines)
                    new_userinfo = get_info()
                    if new_userinfo[username] == salary:
                        str = username + "工资：" + new_userinfo[username]
                        print("修改成功"+ str)
                    else:
                        print("修改失败，请检查输入")

                linenum += 1
        else:
            print("员工 \'"+ username + "\' 不存在")


#插入一行用户信息
def insert_info(username, salary):
    _userinfo = get_info()
    if username in _userinfo:
        str = username + "已经存在!"
        print(str)
    else:
        with open("info.txt", "a", encoding="utf-8") as f:
            f.writelines("\n"+username + ' '  + salary)
        new_userinfo = get_info()
        if new_userinfo[username] == salary:
            str = username + "工资：" + new_userinfo[username]
            print("增加成功" + str)
        else:
            print("增加失败，程序异常")
_fo ='''
1. 查询员工工资
2. 修改员工工资
3. 增加新员工记录
4. 退出
'''

while True:
    _userinfo = get_info()
    print(_fo)
    _user_select1 = input(">>:")
    if not (_user_select1.isdigit()):
        break
    if _user_select1 == '1':
        _user_select_name = input("请输入要查询的员工姓名")

        if _user_select_name in _userinfo:
            str = _user_select_name + "工资：" + _userinfo[_user_select_name]
            print(str)
        else:
            print("员工 \'"+_user_select_name+ "\' 不存在")
            break
    elif _user_select1 == '2':
        _user_select_name = input("请输入要修改的员工姓名和工资，用空格分隔")
        str = _user_select_name
        #str = str.strip()
        str = str.split()
        #print(hehe)
        if len(str) == 2:
            #print(str[1].isdigit())
            username = str[0]
            salary = str[1]
        else:
            print("输入不合规范，请检查")
        update_info(username,salary)
       # print(type(_user_select1))
    elif _user_select1 == '3':
        _user_select_name = input("请输入要增加的员工姓名和工资，用空格分割")
        str = _user_select_name
        str = str.split()
        if len(str) == 2:
            username = str[0]
            salary = str[1]
        else:
            print("输入不合规范，请检查")
        insert_info(username,salary)
    elif _user_select1 == '4':
        exit("再见")
    else:
        print("输入错误的数字")
        break