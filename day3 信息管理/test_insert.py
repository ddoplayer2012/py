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




def insert_info(username, salary):
    _userinfo = get_info()
    if username in _userinfo:
        str = username + "已经存在!"
        print(str)
    else:
        with open("info.txt", "a", encoding="utf-8") as f:
            f.writelines("\n"+username + ' '  + salary)


insert_info('huan1g','5000')