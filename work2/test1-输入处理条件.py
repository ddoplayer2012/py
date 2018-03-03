sql = "select * from aaa where age > 2 and age <10"
key_dict ={
    "where":"",
    "set":""
}
sql_list = sql.split()
action = sql_list[0]
for i in sql_list[1:]:
    if i in key_dict:
        print(sql_list.index(i))
        key_dict[i] = sql_list[sql_list.index(i)+1:]
print(key_dict)