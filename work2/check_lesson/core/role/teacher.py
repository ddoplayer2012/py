#-*- coding:utf-8 -*-



class teacher:
    '''
    教师类：
    member:讲师名，薪资，班级
        1.查询班级
        2.查询学生
    '''

    def __init__(self,teacher_name,teacher_salary,teacher_classes):
        # 存放对象可以避免数据冗余
        self.teacher_name = teacher_name
        self.teacher_salary = teacher_salary
        self.teacher_classes = teacher_classes

    def teacher_add_classes(self,classes_name,classes_obj):

        if self.teacher_classes:
            print("该老师已经有一门在教了，还加课是不是要累死他啊！")
        else:
            self.teacher_classes = classes_obj
