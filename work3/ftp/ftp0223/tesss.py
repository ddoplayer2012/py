import os
from conf import configure as conf


home_prefix = conf.FTP_BASE + '\\' + 'admin'
cmd = "dir %s" % (home_prefix)
file_list = os.popen(cmd).read()
print(file_list)