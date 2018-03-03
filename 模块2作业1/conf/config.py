# -*- encoding:utf-8 -*-
# Author: Koctr


import os


# 数据文件所在的目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 主键
PRIMARY_KEY = "primary key"

# 自增列
AUTO_INCREMENT = "auto increment"

# 数据库配置
DATABASE = {
    'engine': 'file_storage',
    'name': 'staff',
    'path': "%s/db" % BASE_DIR
}

# 表名列表
TABLE_NAMES = ["staff"]

# 列名字典
TABLE_COLUMNS = {
    "staff": ["id", "name", "age", "phone", "dept", "enroll_date"]
}

# 列长度字典
TABLE_COLUMNS_LEN = {
    "staff": {"id": 5, "name": 20, "age": 3, "phone": 11, "dept": 20, "enroll_date": 10}
}

# 列类型字典
TABEL_COLUMNS_TYPE = {
    "staff": {"id": int, "name": str, "age": int, "phone": int, "dept": str, "enroll_date": str}
}

# 表完整性约束
TABLE_CONSTRAINTS = {
    "staff": {PRIMARY_KEY: "phone", AUTO_INCREMENT: "id"}
}
