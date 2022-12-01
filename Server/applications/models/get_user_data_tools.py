from applications.models import user_judgment_tools as uj


# todo 系主任数据获取
def headdepart_data(username, password):
    return_value = {
        'status_code': 200,  # 状态码
        'msg': {
            'error_msg': '',  # 错误信息
        }
    }

    if not username and not password:
        return_value['status_code'] = 400
        return_value['msg']['error_msg'] = '用户名或密码不能为空'
        return return_value

    level = uj.user_get(username, password)['level_info']

    if level['is_headdepart'] == 1:
        pass


# todo 班主任数据获取
def headteacher_data(username, password):
    return_value = {
        'status_code': 200,  # 状态码
        'msg': {
            'error_msg': '',  # 错误信息
        }
    }

    if not username and not password:
        return_value['status_code'] = 400
        return_value['msg']['error_msg'] = '用户名或密码不能为空'
        return return_value

    level = uj.user_get(username, password)['level_info']

    if level['is_headteacher'] == 1:
        pass


# todo 检察员数据获取
def inspector_data(username, password):
    return_value = {
        'status_code': 200,  # 状态码
        'msg': {
            'error_msg': '',  # 错误信息
        }
    }

    if not username and not password:
        return_value['status_code'] = 400
        return_value['msg']['error_msg'] = '用户名或密码不能为空'
        return return_value

    level = uj.user_get(username, password)['level_info']

    if level['is_inspector'] == 1:
        pass
