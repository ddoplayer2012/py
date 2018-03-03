#-*- coding:utf-8 -*-

from core.role.lesson import lesson
from core.role.classes import classes
from core.role.teacher import teacher
from core.role.student import student





class school:
    '''
学校管理类
member:name,address,lesson,classes,teacher
功能：1.增加or更新讲师
    2.增加or更新班级
    3.增加or更新课程

    4.查询讲师
    5.查询班级
    6.查询课程

'''

    def __init__(self,school_name):
        self.school_name = school_name
        #self.school_addr = school_addr
        #key 课程名，value 课程对象实例 ，下面都是类似的存储结构
        self.school_lesson = {}
        self.school_classes = {}
        self.school_teacher = {}

    def add_lesson(self,lesson_name,lesson_price,lesson_period):
        '''
        新建课程给self.school_lesson添加内容，初始化lesson类
        :return:
        '''
        #初始化lesson对象，并存储在school类的school_lesson里
        lesson_obj = lesson(lesson_name,lesson_price,lesson_period)
        self.school_lesson[lesson_name] = lesson_obj

    def add_classes(self,classes_name,lesson_name):
        '''
        新建classes，给self.school_classes添加内容，初始化classes类
        :param classes_name:
        :param lesson_name:
        :return:
        '''
        lesson_obj = self.school_lesson[lesson_name]
        classes_obj = classes(classes_name,lesson_obj)
        self.school_classes[classes_name] = classes_obj

    def add_teacher(self,teacher_name,teacher_salary,teacher_classes):
        '''
        新建teacher类初始化把实例添加到school类的字典里
        :param teacher_name:
        :param teacher_salary:
        :param teacher_classes:
        :return:
        '''
        teacher_obj = teacher(teacher_name,teacher_salary,teacher_classes)
        self.school_teacher[teacher_name] = teacher_obj

    def add_student(self,student_name,student_pass,classes_name):
        '''
        关联学员
        :param student_obj:
        :return:
        '''
        student_obj = student(student_name,student_pass,classes_name)
        self.school_classes[classes_name].classes_student[student_name] = student_obj


    def show_all_lesson(self):
        #打印课程

        for key in self.school_lesson:
            lesson_obj = self.school_lesson[key]
            print("课程名：%s\t价格：%s\t周期：%s 月"%(lesson_obj.lesson_name,lesson_obj.lesson_price,lesson_obj.lesson_period))

    def show_all_classes(self):
        #打印班级
        if self.school_classes:
            for key in self.school_classes:
                classes_obj = self.school_classes[key]
                lesson_obj = classes_obj.lesson_obj
                print("班级名：%s\t关联课程：%s\t课程价格：%s\t课程周期：%s"%(classes_obj.classes_name,lesson_obj.lesson_name,lesson_obj.lesson_price,lesson_obj.lesson_period))
        else:
            print("当前学校没有开班")

    def show_all_teacher(self):
        #打印教师

        for key in self.school_teacher:
            teacher_obj = self.school_teacher[key]
            print("教师名：%s\t薪资：%s\t所授班级：%s\t"%(teacher_obj.teacher_name,teacher_obj.teacher_salary,teacher_obj.teacher_classes))

    def show_classes_student(self):
        #打印班级内的学生
        for key in self.school_classes:
            classes_obj = self.school_classes[key]
            lesson_obj = classes_obj.lesson_obj
            student_obj = classes_obj.classes_student
            for key in student_obj:
                print("学生姓名："+str(key)+"班级名:"+str(student_obj[key].student_classes)+"成绩："+str(student_obj[key].student_grade))

