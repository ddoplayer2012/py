#-*- coding:utf-8 -*-
'''
定义了4个类
'''
import os
import sys
import shelve
from conf import configure
from core.role.school import school
from core.role.classes import classes
import pickle
import pickletools
class school_in(object):
    '''
    学校入口
    :return:
    '''

    def __init__(self,args):
        '''
                   为什么这里要添加回写功能？
                   因为之前用的With,发现出现了bug,本人水平不够无法查错，然后出此策略。
                   '''
        self.username = "游客"
        if os.path.exists(configure.school_db_filepath+".dat"):

             self.school_db = shelve.open(configure.school_db_filepath, flag="c", writeback=True)
             if args == 'admin':
                 self.admin_manage()
             elif args == 'student':
                 self.student_manage()
             elif args == 'teacher':
                 self.teacher_manage()
             else:
                print("程序异常！位置：schoo_in初始化处")
        else:
            print("数据库文件不存在，正在初始化")
            self.init_school_db()


    def init_school_db(self):
        '''
        初始化数据库表结构
        北京：pyhton,linux
        上海：go
        :return:
        '''
        self.school_db = shelve.open(configure.school_db_filepath,flag="c",writeback=True)
        t1 = school('北京')
        t2 = school('上海')
        self.school_db['北京'] = t1
        self.school_db['上海'] = t2
        t1.add_lesson("python",8888,8)
        t1.add_lesson("linux",9999,8)
        t1.add_classes("c1","python")
        t1.add_teacher('alex',888888,"c1")
       # t1.add_student('me',123456,"c1")
       # t1.add_student('you',123456,"c1")
        t2.add_lesson("GO",18888,8)
        #self.school_db.update({t1.school_name: t1})
        #self.school_db.update({t2.school_name: t2})
        #self.school_db.close()

    #、学员、课程、讲师、班级
    def admin_manage(self):
        '''
        学校管理视图
        1.选择学校
        2.学校管理
        3.读取数据库到变量
        :return:
        '''
        while True:
            for key,v in self.school_db.items():
                print('当前学校有:',key)
            select_school = input("请输入需要管理的学校名：").strip()
            if select_school in self.school_db.keys():
                self.select_school = select_school
                self.school_object = self.school_db[select_school]
                while True:
                    info = '''欢迎进入%s管理信息系统
                              1.创建课程
                              2.创建班级
                              3.创建讲师
                              4.查询课程
                              5.查询班级
                              6.查询讲师
                              7.查询学员
                              q.退出
                                      '''%(self.select_school)
                    print(info)
                    menu = {
                        "1": self.create_lesson,
                        "2": self.create_classes,
                        "3": self.create_teacher,
                        "4": self.show_lesson,
                        "5": self.show_classes,
                        "6": self.show_teacher,
                        "7": self.show_student,
                        "q": self.quit_subsystem }
                    select_menu = input('选择管理选项：').strip()
                    if select_menu in menu:
                        menu[select_menu]()
                        input("Press Enter key to continue")
                    else:
                        print('输入有误，请重试')
            else:
                print('该学校%s不存在！'%(select_school))
    def show_student(self):
        '''
        查询学员
        :return:
        '''
        self.school_object.show_classes_student()

    def  create_classes(self):
        '''
        创建班级，调用school类的add_classes来创建
        :return:
        '''
        classes_name = input('输入要创建的班级名称：').strip()
        lesson_name = input('输入要关联的课程名称：').strip()
        #判断班级是否存在
        if classes_name in self.school_object.school_classes:
            print('班级已经存在,将自动更新覆盖')
            self.school_object.add_classes(classes_name,lesson_name)
            print('已更新班级内容')
        elif lesson_name not in self.school_object.school_lesson:
            print('课程%s不存在'%lesson_name)
        else:
            self.school_object.add_classes(classes_name,lesson_name)
            print('已创建班级:%s'%classes_name)
        #self.school_db.update({self.select_school:self.school_object})
        self.school_db = {self.select_school:self.school_object}




    def create_lesson(self):
        '''
        创建课程，调用school类的add_lesson来创建课程
        :return:
        '''

        lesson_name = input('输入要创建的课程名称：').strip()
        lesson_price = input('输入要创建的课程价格：').strip()
        lesson_period = input('输入要创建的课程周期').strip()
        if lesson_name in self.school_object.school_lesson:
            print('该课程已经存在')
            self.school_object.add_lesson(lesson_name,lesson_price,lesson_period)
            print('已更新课程%s',lesson_name)
        else:
            self.school_object.add_lesson(lesson_name, lesson_price, lesson_period)
            print('已创建课程%s'%lesson_name)
        #更新数据库
        #self.school_db.update({self.select_school:self.school_object})
        self.school_db = {self.select_school: self.school_object}

    def create_teacher(self):
        '''
        创建教师，调用school类的add-teacher来创建教师
        :return:
        '''
        teacher_name = input('输入老师的姓名：').strip()
        teacher_salary = input('输入老师的薪资：').strip()
        teacher_classes = input('输入老师带的班级：').strip()
        if teacher_classes in self.school_object.school_classes:
            #班级名的实例
            obj_classes = self.school_object.school_classes[teacher_classes]
            if teacher_name not in self.school_object.school_teacher:
                self.school_object.add_teacher(teacher_name,teacher_salary,teacher_classes)
                print('已招聘新的老师:%s'%teacher_name)
            else:
                self.school_object.add_teacher(teacher_name,teacher_salary,teacher_classes)
                print('已更新老师%s'%teacher_name)
            #self.school_db.update({self.select_school: self.school_object})
            self.school_db = {self.select_school: self.school_object}
        else:
            print('该班级%s不存在'%teacher_classes)

    def show_lesson(self):
        #打印课程
        self.school_object.show_all_lesson()
    def show_classes(self):
        #打印班级
        self.school_object.show_all_classes()
    def show_teacher(self):
        #打印教师
        self.school_object.show_all_teacher()

    def student_manage(self):
        '''
        学生视图
        :return:
        '''
        while True:
            for key, v in self.school_db.items():
                print('当前学校有:', key)
            select_school = input("请输入需要报名的学校名：").strip()
            if select_school in self.school_db.keys():
                self.select_school = select_school
                self.school_object = self.school_db[select_school]

                while True:
                    if self.username == '游客':
                        info = '''欢迎[%s]进入%s学校咨询
                                  1.查询课程
                                  2.查询班级
                                  3.查询讲师
                                  4.报名参课
                                  5.已报名学员登录账号
                                  q.退出
                                          ''' % (self.username, self.select_school)
                        menu = {
                            "4": self.join_lesson,
                            "1": self.show_lesson,
                            "2": self.show_classes,
                            "3": self.show_teacher,
                            "5": self.student_login,
                            "q": self.quit_subsystem
                                }


                    else:
                        self.cur_classes_obj = self.get_classes_obj(self.username)
                        count = 0
                        lesson_name = self.cur_classes_obj.lesson_obj.lesson_name
                        info = '''欢迎[%s]进入%s学校%s班级%s
                                    1.查询成绩
                                    x.注销登录
                                    q.退出
                                            ''' % (self.username, self.select_school,self.cur_classes_obj.classes_name,lesson_name)
                        menu = {
                            "1": self.show_grade,
                            "x": self.log_off,
                            "q": self.quit_subsystem}

                    print("\033[34;0m" + info + "\033[0m")
                    select_menu = input('选择操作选项：').strip()
                    if select_menu in menu:
                        menu[select_menu]()

                    else:
                        print('输入有误，请重试')
            else:
                print('该学校%s不存在！' % (select_school))

    def log_off(self):
        #注销
        if self.username == '游客':
            print('当前状态未登录，不能注销')
        else:
            self.username = "游客"


    def join_lesson(self):
        for key in self.school_object.school_classes:
            classes_obj = self.school_object.school_classes[key]
            lesson_obj = classes_obj.lesson_obj
        print("当前已开授班级目录：%s\t关联课程：%s\t课程价格：%s\t课程周期：%s" % (
            classes_obj.classes_name, lesson_obj.lesson_name, lesson_obj.lesson_price, lesson_obj.lesson_period))
        while True:
            classes_select = input("请选择班级名称：")
            if classes_select in self.school_object.school_classes:
                cur_classes_obj = self.school_object.school_classes[classes_select]
                break
            else:
                print("当前班级不存在!请重试")

        info = '''
        您选择了 %s  班级
        属于  %s     系列
        价格  %s     元
        学习时间 %s  个月
        ''' % (
            classes_select, cur_classes_obj.lesson_obj.lesson_name, cur_classes_obj.lesson_obj.lesson_price,
            cur_classes_obj.lesson_obj.lesson_period)
        print(info)
        # self.sutdent_login(classes_obj)
        # 学员交费注册
        username = input("输入学员姓名进行报名：")
        password = input("输入注册密码：")
        register = input("是否进行支付宝交费？y/n")
        if register == 'y' or register == 'Y':
            pay_result = self.student_register()
            if pay_result == True:
                # 支付成功,注册学籍
                self.school_object.add_student(username, password, classes_select)
                # 自动登录
                self.username = username
        else:
            print("注册失败,仍是游客身份")

        #self.school_db.update({self.select_school: self.school_object})

    def student_register(self):
        # 模拟支付宝支付
        return True
    def show_grade(self):
        '''
        打印成绩
        :return:
        '''
        self.cur_classes_obj.classes_student[self.username].show_your_grade()

    def get_classes_obj(self,student_name):
        '''
        获取classes对象
        :param student_name:
        :return:返回 classes对象
        '''
        for key, val in self.school_object.school_classes.items():
            for k in val.classes_student:
                if student_name in k:
                    student_classes = val.classes_student[k].student_classes
                    get_classes_obj = self.school_object.school_classes[student_classes]
                    return get_classes_obj
    def student_login(self):
        print("欢迎登录")
        username = input("输入学员姓名：")
        password = input("输入登录密码：")
        #查询用户名合法性。。。如果老师有更好的思路，请通知我修改一下。
        for key,val in self.school_object.school_classes.items():
             for k in val.classes_student:
                 if username in k:
                     if val.classes_student[k].student_pass == password:
                        print("密码正确，登录成功")
                        self.username = username
                        break
                     else:
                         print("登录失败，密码错误")
                     break
                 else:
                     print("用户名不存在")

    def teacher_manage(self):
        '''
        教师视图
        选择班级进行管理show_classes
        查询班级下的学生
        修改学生成绩
        查询学生成绩
        :return:
        '''
        while True:
            for key, v in self.school_db.items():
                print('当前学校有:', key)
            select_school = input("请输入需要管理的学校名：").strip()
            if select_school in self.school_db.keys():
                self.select_school = select_school
                self.school_object = self.school_db[select_school]
                #先登录，后管理
                print("需要登录获取教师管理功能")
                while True:
                    teacher_name = input("输入教师姓名：")
                    passwd =input("请输出教师密码：")
                    #时间不够，不写登录模块了
                    password = ""
                    if teacher_name in self.school_object.school_teacher:
                        self.teacher_object = self.school_object.school_teacher[teacher_name]
                        if password == passwd:
                            print('登录成功')
                            break
                        else:
                            print('密码错误')
                    else:
                        print('该教师不存在')


                #打印班级，进入班级管理

                while True:
                    info = '''欢迎进入%s管理信息系统
                                     1.创建课程
                                     2.创建班级
                                     4.查询课程
                                     5.查询班级
                                     6.评分成绩
                                     7.查询学员
                                     
                                     q.退出
                                             ''' % (self.select_school)
                    print(info)
                    self.show_cur_classes()
                    menu = {
                        "1": self.create_lesson,
                        "2": self.create_classes,
                        "3": self.create_teacher,
                        "4": self.show_lesson,
                        "5": self.show_cur_classes,
                        "6": self.set_student_grade,
                        "7": self.show_student,
                        "q": self.quit_subsystem}
                    select_menu = input('选择管理选项：').strip()
                    if select_menu in menu:
                        menu[select_menu]()
                        input("Press Enter key to continue")
                    else:
                        print('输入有误，请重试')
            else:
                print('该学校%s不存在！' % (select_school))
    def set_student_grade(self):
        '''
        评分学生成绩
        :return:
        '''
        self.show_student()
        classes_name = self.teacher_object.teacher_classes
        self.classes_obj = self.school_object.school_classes[classes_name]
        self.student_obj = self.classes_obj.classes_student
        classes_obj = self.classes_obj
        student_name = input("请输入同学姓名：")
        if  student_name in self.student_obj:
            student_grade = input('输入评分：')
            self.student_obj[student_name].student_grade = student_grade
            self.school_db = {self.select_school: self.school_object}
        else:
            print('请输入正确的学生姓名')

    def show_cur_classes(self):
        '''
        显示当前教的班级
        :return:
        '''
        classes_name = self.teacher_object.teacher_classes
        self.classes_obj = self.school_object.school_classes[classes_name]
        classes_obj = self.classes_obj
        self.lesson_obj = self.classes_obj.lesson_obj
        lesson_obj =  self.lesson_obj

        if self.classes_obj:
            print("授课人：%s\t班级名：%s\t关联课程：%s\t课程价格：%s\t课程周期：%s"%(self.teacher_object.teacher_name,classes_obj.classes_name,lesson_obj.lesson_name,lesson_obj.lesson_price,lesson_obj.lesson_period))
        else:
            print("当前学校没有开班")
    def student_info(self):
        print("欢迎查询个人信息")

    def quit_subsystem(self):
        self.school_db.close()
        exit('退出')


def quit_system():
    '''
    结束程序
    :return:
    '''
    print("\033[31;1m退出系统\033[0m")
    exit()

class admin_center(object):
    def __init__(self):
        pass

    def start(self):
        while True:
            info = '''
          欢迎进入学校管理信息系统
        
            1.学生入口
            2.教师入口
            3.管理员入口
            q.退出
            '''
            menu = {
                "1": "student",
                "2": "teacher",
                "3": "admin",

            }
            print(info)
            user_select = input("请选择要登录的入口:")

            if user_select in menu.keys():
                school_in(menu[user_select])
            elif user_select == 'q':
                quit_system()
            else:
                print("请根据菜单进行选择")


t1 = admin_center()
t1.start()