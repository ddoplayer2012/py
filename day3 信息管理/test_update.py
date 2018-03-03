def get_info():
    userinfo = {}
    with open("info.txt","r",encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        line = line.split(" ")
       #print(line[0])
        userinfo[line[0]] =line[1]
    return userinfo

def update_info(username):
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
                    _user_update = input("请输入要修改的员工姓名和工资，用空格分隔")
                    lines[linenum] = _user_update +"\n"
                    with open("info.txt", "w", encoding="utf-8") as fw:
                        fw.writelines(lines)
                linenum += 1
        else:
            print("员工 \'"+ username + "\' 不存在")


update_info("Alex")
#with open("info.txt", "w", encoding="utf-8") as fw:

