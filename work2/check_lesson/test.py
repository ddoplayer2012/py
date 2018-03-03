import os
import sys
import shelve
from conf import configure
from core.role.school import school


class admin_in(object):
    '''
    学校管理视图
    :return:
    '''

    def __init__(self):
        if os.path.exists(configure.school_db_filepath + ".dat"):
                with shelve.open(configure.school_db_filepath) as self.school_db:
                    self.admin_manage()
               # self.school_db.close()
        else:
            print("数据库文件不存在，正在初始化")
            self.init_school_db()
            self.admin_manage()

    def init_school_db(self):
        '''
        beijing,shanghai
        :return:
        '''
        self.school_db = shelve.open(configure.school_db_filepath)
        self.school_db['北京'] = school('北京', '北京市沙河培训基地')
        self.school_db['上海'] = school('上海', '上海市外滩培训基地')

    def admin_manage(self):
        '''
        学校管理视图
        :return:
        '''

        print("")

d1 = admin_in()