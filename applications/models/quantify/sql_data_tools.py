import pymysql

from applications.common.quantify import setting as st
from applications.models.quantify import file_data_tools as ft


# 全局查询函数 global_query
def global_query(sql):
    """
    > The function `global_query` is used to query data from the database

    :param sql: The SQL statement to be executed
    :return: The result of the query.
    """
    """ 查询：全局 """
    conn = pymysql.connect(**st.MYSQL_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
    except Exception as e:
        err_msg = f'Query Error! Sql:{sql}, Error:{e}'
        return err_msg
    finally:
        conn.close()


# 规则查询函数 rule_query
def rule_query(tb_name, field, filter_sql=True, format_sql=True, db_name=st.DB_NAME):
    """
    :param tb_name: table name
    :param field: The field to be queried, which can be a list or a string
    :param filter_sql: Whether to filter the fields, if True, the fields in the field parameter will be filtered out,
    defaults to True (optional)
    :param format_sql: Whether to format the sql statement, the default is True, defaults to True (optional)
    :param db_name: The database name, which is the default database name in the configuration file
    :return: the SQL query that is being generated.
    """

    """ 查询：规则 """

    # 判断是否需要过滤字段
    if filter_sql:

        # 判断deprecated_fields是否为list类型,如果不是则转换为list类型
        if not isinstance(field, list):
            field = [field]

        # 查询表结构
        sql = f'''
        SELECT CONCAT('select ', GROUP_CONCAT(COLUMN_NAME), ' from ', TABLE_NAME)
        FROM information_schema.COLUMNS
        WHERE table_name = '{tb_name}'
        AND TABLE_SCHEMA = '{db_name}'
        '''

        # 拼接sql语句
        for i in field:
            sql += f'AND COLUMN_NAME != \'{i}\'' if i != field[-1] else f' AND COLUMN_NAME != \'{i}\''

        sql = global_query(sql)[0][0]

        # 返回sql语句
        sql = sql.replace('\n', '').lstrip(' '). \
            replace('select ', 'select `').replace(',', '`,`').replace(' from ', '` from ') \
            if format_sql else sql.replace('\n', '').lstrip(' ')

        return sql

    else:
        # 便利field为查询的字段
        if isinstance(field, list):
            field = ','.join(field)

        # 判断是否需要格式化sql语句

        # 创建表结构
        sql = f'''
        select {field} from {tb_name}
        '''

        # 返回sql语句
        sql = sql.replace('\n', '').lstrip(' '). \
            replace('select ', 'select `').replace(',', '`,`').replace(' from ', '` from ') \
            if format_sql else sql.replace('\n', '').lstrip(' ')

        return sql


# 修改函数 global_modify
def global_modify(sql):
    """
    It takes a string as an argument and returns a string.

    :param sql: The SQL statement to be executed
    """
    """ 修改：插入、更新、删除 """
    conn = pymysql.connect(**st.MYSQL_CONFIG)

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            return 1
    except Exception as e:
        print(f'Modify Error! Sql:{sql}, Error:{e}')
        return -1
    finally:
        conn.close()


# 解析sql文件
def parse_sql_file(file_path):
    """
    > This function takes a file path as an argument and returns a list of SQL queries

    :param file_path: The path to the file you want to parse
    """

    with open(file_path, 'r', encoding='utf-8') as f:
        res = [_ for _ in ''.join(
            [_.strip('\n') for _ in f.readlines() if not _.lstrip('\n').startswith('--') and _.strip('\n') != '']
        ).split(';') if _ != '']
    return res


# 服务层
# 执行sql文件 exec_sql_file
def exec_sql_file(file_path):
    """
    This function takes a file path as an argument and returns a table of the data in the file.

    :param file_path: The path to the file you want to create a table for
    """

    """ 读取sql，创建表 """

    sql_file = ft.get_file(file_path, 0, '.sql')['file_path']
    sql_list = parse_sql_file(sql_file)

    conn = pymysql.connect(**st.MYSQL_CONFIG)

    for sql in sql_list:
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
                return 1
        except Exception as e:
            print(f'Create Error! Sql:{sql}, Error:{e}')
            return -1
        finally:
            conn.close()


if __name__ == '__main__':
    test = rule_query(
        'user', ['username', 'password'], False, True
    )
    print(test)
