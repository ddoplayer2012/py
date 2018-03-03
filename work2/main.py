import collections
import re
def sql_to_dict(sql,key_list):
    '''用来根据关键字转换为字典传出
    eg: {'select': '*', 'where': 'empno=7396', 'from': 'emp'}
    :param sql:
    :param key_list:
    :return:
    '''
    sql_list = []
    sql_dic = {}
    for i in key_list:
        #print(sql.split(i))
        b = [ key.strip() for key in sql.split(i) ]
        #len(b)>1则说明分割成功，取到了关键字
        if len(b) > 1:
            if len(sql.split('limit')) > 1:
                print("暂时未开发limit功能")
            if i == 'where' or i == 'values':
                sql_dic[i] = 'where'+b[-1]
            if sql_list:
                sql_dic[sql_list[-1]] = b[0]
            sql_list.append(i)
            sql = b[-1]
        else:
            sql = b[0]
        if sql_dic.get("select"):
            #如果没找到from 关键字和where关键字--如果from在key_lis位置靠后，会造成多次循环，这里手动添加from字典
            if not sql_dic.get("from") and not sql_dic.get("where"):
                #print("sql没有from和where",sql_dic.get("select"))
                sql_dic['from'] = b[-1]
                #print ("add" ,sql_dic.get ("select"))
    if sql_dic.get('select'):
        #找到select后关键字保存到字典里
       # print("ehhe")
        #print(sql_dic.get('select').split(','))
        sql_dic['select'] = sql_dic.get('select').split(',')
        #print(sql_dic['select'])
    if sql_dic.get('where'):
        pass
        #sql_dic['where'] = where_to_dict1(sql)
    return (sql_dic)

def where_to_dict(where):
    '''
    分割where后面的语句或set后面语句
    :param where:
    :return:
    '''
    key_dict = {
        "where": "",
        "set": ""
    }
    sql_list = where.split ()
    #action = sql_list[0]
    for i in sql_list[1:]:
        if i in key_dict:
            #print (sql_list.index (i))
            key_dict[i] = sql_list[sql_list.index (i) + 1:]
    return key_dict


def where_complex(where_sql):
    '''
    条件复制起来
    :return:
    '''

    test = where_sql
    count = 1
    test_list = []
    flag_list = []
    all_list = []
    for i in range(len(test)):
        # print (count % 3)
        if count % 4 != 0:
            test_list.append(test[i])
        else:
            flag_list.append(test[i])
            all_list.append(test_list)
            test_list = []
        count += 1
    if test_list != []:
        all_list.append(test_list)
        test_list = []
    if "where" in flag_list:
        pass
    return all_list, flag_list

def parse_all(where_sql,where_and):
    '''
    用来复制粘贴到一起
    :param where_sql:
    :param where_and:
    :return:
    '''
    where_all = []
    for i in range(len(where_and)):
        if len(where_sql) - 1 == len(where_and):
            where_all.append(where_sql[i])
            where_all.append(where_and[i])
        if i == len(where_and) - 1:
            where_all.append(where_sql[i + 1])
    return where_all

def file_in_dict(str):
    dictfield = {}
    fieldstr = str.split(",")
    for i in range(len(fieldstr)):
        dictfield[field[i]] = fieldstr[i]
    return dictfield

if __name__ == "__main__":
    #1,Alex Li,22,13651054608,IT,2013-04-01
    field = ["id","name","age","phone","job","hiredate"]
    with open("staff_data","r",encoding="utf-8") as f:
        key_lis = ['select', 'insert', 'delete', 'update', 'from', 'into', 'set', 'values', 'where', 'limit']
   # while True:
        #sql_ ="select empno from emp where empno = 7396 and ename = \'smith\' and json like \'hehe\' or hehe = 'heihei'"
        sql_ = "select name,age,phone from staff_data where age > 22 "
        print(sql_)
        sql = re.sub(' ',"", sql_)
        #print(sql)
        if len(sql) == 0: pass
        if sql == "exit": exit('结束程序')
        sql_dict = sql_to_dict(sql,key_lis)
        where_dict = where_to_dict(sql_)
        if   where_dict["set" ] == "":
            where_sql,where_and = where_complex(where_dict["where"])
            print(where_sql)
            sql_dict['where'] = where_sql
            print(sql_dict)
        staff_id = 1231234123
        menmory = {}
        for key in f.readlines():
            dicts = file_in_dict(key)
            menmory[staff_id] = dicts
            staff_id += 1
        menmory =collections.OrderedDict(menmory)
        for i in range(len(where_sql)):
            if sql_dict["select"] == "*":
                for k, v in menmory.items():
                    if where_sql[i][1] == '>':
                       if v[where_sql[i][0]] > where_sql[i][2]:
                           print(v)
            else:
                for k, v in menmory.items():
                    if where_sql[i][1] == '>':
                        if v[where_sql[i][0]] > where_sql[i][2]:
                           for k in range(len(sql_dict['select'])):
                            print(v[sql_dict['select'][k]],end ='\t')
                        print("")
