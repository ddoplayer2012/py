#-*- coding:utf-8 -*-


class student(object):
    '''
    学生类：
    1.查询学校
    2.选择学校
    3.查询课程
    4.选择班级
    '''

    def __init__(self,student_name,student_pass,student_classes):
        self.student_name = student_name
        self.student_pass = student_pass
        self.student_classes = student_classes
        self.student_grade = 0



    def add_money(self,push_money):
        '''
        支付宝充钱,假设学员的支付宝是无限的。。。。。。
        :param push_money:
        :return:
        '''
        self.student_zhifubao_money += push_money


    def show_your_grade(self):
        print("上次测试成绩为："+str(self.student_grade))

    def register_school_member(self,classes_obj):
        '''
        注册学籍
        :param school_obj:
        :return:
        '''
        if self.student_zhifubao_money >= classes_obj.lesson_obj.lesson_price:
            self.student_zhifubao_money -= classes_obj.lesson_obj.lesson_price
            classes_obj.classes_student[self.student_name] = self
            print("注册学籍成功")
