from applications.common import mysql_conn as conf

# 配置文件

# mysql数据库配置
try:
    MYSQL_CONFIG = conf.get_mysql_conn('../../conf/key')
except:
    MYSQL_CONFIG = conf.get_mysql_conn('./conf/key')

# {
#     # 'host':'127.0.0.1',
#     'host': '101.43.61.66',
#     'port': 3306,
#     'user': 'root',
#     'password': 'weston987',
#     'database': 'cls_sys',
#     'charset': 'utf8',
# }


# # 数据库名称
DB_NAME = 'cls_sys'
# 数据库表
TABLE_人员表 = 'user'
# TABLE_班主任表 = 'person_headteacher'
# TABLE_系主任表 = 'person_headdepart'
# TABLE_检查员表 = 'person_inspector'
TABLE_班级表 = 'inspect_class'
TABLE_检查结果表 = 'inspect_result'
TABLE_检查项目表 = "inspect_items"

# 人员类型
ptype_班主任 = 'bzr'
ptype_系主任 = 'xzr'
ptype_检查员 = 'jcy'
