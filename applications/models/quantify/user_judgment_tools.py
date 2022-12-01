import re

from applications.common.quantify import setting as st
from applications.models.quantify import sql_data_tools as us, data_processing_tools as dp


def user_get(username=None, password=None):
    user_info = us.rule_query(
        st.TABLE_人员表, ['username', 'password', 'depart', 'token', 'create_time', 'update_time'], True, False
    )

    # 拆分查询语句字段-数据处理
    # 判断 fields 中的值是否有存在 `` 如果有则去除

    # fields = [i[1:-1] if i[0] == '`' and i[-1] == '`' else i for i in dp.build_field(info)]

    fields = [i for i in dp.build_field(user_info) if re.match(r'^is', i)]

    user_list = []
    permission_level = ''

    for i in fields:
        fields_info = us.rule_query(
            st.TABLE_人员表, f'{i}', False, True
        )

        # (SQL > 拼接SQL用于获取 `fields_info` 中的数据)
        sql = f'''
            {fields_info} where `username` = '{username}' and `password` = '{password}'
        '''

        # (1 将获取的信息追加到 user_list 中)
        user_list.append(us.global_query(sql)[0][0])

        # (2 数据格式转换 list -> dict)
        user_dict = dict(zip(fields, user_list))

        # 复制获取的数据
        permission_level = user_dict.copy()

    # (SQL > 获取字段 `permission_level` 的全部值去重后并赋值给 permission_level_list 类型为 list )
    sql = f'''
            select distinct `permission_level` from {st.TABLE_人员表}
            '''

    # 语句变更为：select distinct `permission_level` from `人员表`
    permission_level_uid_list = [i[0] for i in us.global_query(sql)]

    # (SQL > 根据字段 `permission_level` 来获取对应的权限值)
    sql = f'''
            select distinct 
            `permission_level` from {st.TABLE_人员表} where `username` = '{username}' and `password` = '{password}'
    '''
    permission_level_uid = us.global_query(sql)[0][0]

    # (SQL > 根据字段 `inspector_id` 来获取对应的权限值)

    res = {
        'level_list': permission_level_uid_list,
        'level_user': permission_level_uid,
        'level_info': permission_level,
    }

    return res


def user_ops(username=None, password=None):
    level = user_get(username, password)

    level_info = level['level_info']

    return_value = {
        'status_code': 200,  # 状态码
        'msg': {
            'error_msg': '',  # 错误信息
            'user_info': '',  # 用户信息
        }
    }

    if not username and not password:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '用户名或密码为空'
        return return_value

    if level_info['is_headdepart'] == 1:
        sql = f'''
            update {st.TABLE_人员表} set 
            `permission_level` = 3 where `username` = '{username}' and `password` = '{password}'
        '''
        us.global_modify(sql)
        return_value['msg']['user_info'] = '权限已修改为系主任：level->3'
    elif level_info['is_headteacher'] == 1:
        sql = f'''
            update {st.TABLE_人员表} set 
            `permission_level` = 2 where `username` = '{username}' and `password` = '{password}'
        '''
        us.global_modify(sql)
        return_value['msg']['user_info'] = '权限已修改为班主任：level->2'
    elif level_info['is_inspector'] == 1:
        sql = f'''
            update {st.TABLE_人员表} set 
            `permission_level` = 1 where `username` = '{username}' and `password` = '{password}'
        '''
        us.global_modify(sql)
        return_value['msg']['user_info'] = '权限已修改为检察员：level->1'
    else:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '权限不足'
        return return_value

    # todo 逻辑线程更新 变更为 init.py 中的线程更新

    return return_value


def user_res(username=None, password=None):
    # (SQL > -/检察员验证/- 根据权限获取ID)

    level = user_get(username, password)

    level_user = level['level_user']
    level_info = level['level_info']

    return_value = {
        'status_code': 200,  # 状态码
        'msg': {
            'error_msg': '',  # 错误信息
            'user_info': '',  # 用户信息
        }
    }

    res = {
        'status_code': 200,  # 状态码
        'msg': '',  # 用户信息
    }

    if not username and not password:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '用户名或密码为空'
        return

    if level_info['is_headdepart'] == 1:
        del return_value['msg']['error_msg']

        # (User -/系主任/- 获取系主任所在系的所有班级)

        sql = us.global_query(f'''
        {us.rule_query(
            st.TABLE_检查结果表, ['create_time', 'update_time'], True, True
        )}
        ''')

        if not sql:
            res['status_code'] = 404
            res['msg'] = '暂无数据'
            return res

        # sql = [i.replace('\n', '').replace('  ', '').replace(',', ', ') if isinstance(i, str) else i for i in sql[0]]

        res['msg'] = sql

    elif level_info['is_headteacher'] or level_info['is_inspector'] == 1:
        del return_value['msg']['error_msg']

        # (User -/班主任/- 获取班主任所在班级的所有学生)

        uid = us.global_query(sql=f'''
        {us.rule_query(
            st.TABLE_人员表, ['id'], False, True
        )} where `permission_level` = {level_user} and `username` = '{username}' and `password` = '{password}'
        ''')

        # (SQL > 根据ID获取数据)
        sql = us.global_query(f'''
        {us.rule_query(
            st.TABLE_检查结果表, ['create_time', 'update_time'], True, True
        )} where `user_id` = {uid[0][0]}
        ''')

        if not sql:
            res['status_code'] = 404
            res['msg'] = '暂无数据'
            return res

        # sql = [i.replace('\n', '').replace('  ', '').replace(',', ', ') if isinstance(i, str) else i for i in sql[0]]

        res['msg'] = sql

    else:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '权限不足'
        return return_value

    return res


if __name__ == '__main__':
    test = user_res('吴洁', 'wujie321')
    # test = user_res('王璐', 'wanglu321')
    # test = user_res('demo', 'demo')
    # test = user_get('demo2', 'demo2')
    print(test, '\n', '--' * 20)
