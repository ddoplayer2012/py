import os
import time


f =open("E:\\py\\work3\\ftp0218\\ftpfiles\\admin\\test.txt.tmp", "rb")
size = 99
print(f.readline())
q =open("d:\\test.txt", "rb")
print(q.readline())
c = 0

print(size)
q.seek(size,0)
for line in q :
    print(line)
print(q.readline())
print(q.readline(c-1))

f.close()
q.close()


'''
l\xd3W\xc5Ah`\x1e\x96En\xe8@\xd8\xcd\xf9\xfb\xa3\xcc\xbfv\xc1Mg#X\xba\xe2|\x08\xcaBgDD\x9c\xb76\x18\xa4\xc2'E\xe00\xd5\x1f\x16\xa3\x95\x8f\xf1\t\xd9:\xd6\x9b\x83YJ~&\x90\xeb\x9e\x02\x8d?\xfa'4\xf5\xdf\x1fMS}\xb7\x11\x1a^xz\xfd\xb3\xb4<k4G*y\x03s\x9c/F\xd9\xa7\x98$\x8d\xef\xf7e\xdb?\x9bT\x9a\xf6\xcf&\xff\xa3,\xfb\x81s\xe0U\xe3\xa3\xf4\xdbz\x05\xfc~\x9d\x02\xaa}\x02*\x8d\xfa\xf04\xde\x88M\xbf\xd2X\x7fSV\xf9\xed\x8d\xf2t6|\xcb\xbce\xafQb\xe6\xe7P\xf1Od\xff\xd1y\xcbo\xce\x00\xb4!\xfe\xfb\xde\xfd\x07\xf7D\xfe\xe7\xfb\x0f\xef\xdd\xdfC\xfb\xcf\xc3{\x9f\xf3\xff\xfek\xec?F\xe4wS<\xcf\n
'''