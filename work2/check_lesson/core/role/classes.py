#-*- coding:utf-8 -*-

from core.role.student import student
class classes(object):
    '''
    班级类
    member:名称，课程对象，学生字典
    '''
    def __init__(self,classes_name,lesson_obj):
        self.classes_name = classes_name
        self.lesson_obj = lesson_obj
        #学生字典{学生名：学生实例}
        self.classes_student = {}

