import os
from dotenv import dotenv_values

config = dotenv_values('.flaskenv')

# 量化管理系统配置
MYSQL_CONFIG = {
    'host': config.get('MYSQL_HOST') or '101.43.61.66',
    'user': config.get('MYSQL_USERNAME') or 'root',
    'password': config.get('MYSQL_PASSWORD') or 'weston987',
    'database': config.get('MYSQL_DATABASE') or 'pear_admin_flask',
    'port': int(config.get('MYSQL_PORT')) or 3306,
    'charset': 'utf8mb4',
    # 'ssl': {'ca': file.get_all_file(file_path, 0, '.pem')['file_path'], },
}

# # 数据库名称
DB_NAME = 'cls_sys'
# 数据库表
TABLE_人员表 = 'user'
# TABLE_班主任表 = 'person_headteacher'
# TABLE_系主任表 = 'person_headdepart'
# TABLE_检查员表 = 'person_inspector'
TABLE_班级表 = 'inspect_class'
TABLE_检查结果表 = 'inspect_result'
TABLE_检查项目表 = 'inspect_items'

# 人员类型
ptype_班主任 = 'bzr'
ptype_系主任 = 'xzr'
ptype_检查员 = 'jcy'
