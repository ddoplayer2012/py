import collections
# 关键字条件过滤
aa = {12312312312:{"name":"alex","age":22,"de[t":"IT","enroll_date":"xxxx","staff_id":"xxxxx"}}

#主键  12312312312
listx =[]
for k,v in aa.items():
    for k1,v1 in v.items():#k1 name v1:alex,k1作为字段名,v1作为字段值
        if k1 == 'name' or k1 == 'age':
            listx.append(v1)

print( listx)


#关键字条件判断
#like "2013"字符串
print("20" in "2013")
#like

#
bb = collections.OrderedDict(aa)
print (bb)