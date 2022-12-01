import ast
import json

from applications.common import setting as st
from applications.models import utils_others_tools as uo, data_processing_tools as dp, sql_data_tools as us, \
    user_judgment_tools as uj


def index_check(username=None, password=None):
    user_info = class_check(username, password)

    # Bar_options = pyecharts_bar.cou_base()

    # Cloud_options = pyecharts_bar.wordcloudpic()

    return_value = {
        'status_code': 200,  # 状态码
        'msg': {
            # 'images': images.images(),  # 照片和个人简介
            # 'Bar_options': Bar_options.dump_options(),  # 柱状图
            # 'Cloud_options': Cloud_options.dump_options(),  # 词云图
            'user_data': user_info  # 用户数据

        }
    }

    return return_value['msg']


def login_check(username, password):
    """
    A function that checks whether the username and password are correct.

    :param username: 用户名
    :param password: The password of the user
    :return: A dictionary with the following keys:
        status_code: 200
        msg:
            error_msg: ''
            token: ''
            user_id: ''
            name: ''
            is_headdepart: ''
            is_headteacher: ''
            is_inspector: ''
            permission_level: ''
    """

    # 构建[return_value]用于返回数据
    return_value = {
        'status_code': 200,  # 状态码
        'msg': {
            'error_msg': '',  # 错误信息
            'token': '',  # token之
            'user_id': '',  # 用户ID
            'name': '',  # 用户名
            'is_headdepart': '',  # 是否系主任
            'is_headteacher': '',  # 是否班主任
            'is_inspector': '',  # 是否检查员
            'permission_level': ''  # 权限等级
        }
    }

    # 使用规则查询查询获 setting 中 {st.TABLE_检查结果表} 的 table_name
    # (1 排除 `username`, `password`, `depart`, `token`, `create_time`, `update_time` 字段
    # (2 语句是格式化: False (否)
    info = us.rule_query(
        st.TABLE_人员表, ['username', 'password', 'depart', 'token', 'create_time', 'update_time'], True, False
    )

    # 拆分查询语句字段-数据处理
    fields: object = dp.build_field(info)

    # 验证基本登录信息-数据校验
    if not username or not password:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '用户名或密码为空！'
        return return_value

    # 数据库查询语句A
    # 使用 SQL 查询字段 `username` 来查找是否存在该用户
    sql = f'''
    select `username` from {st.TABLE_人员表} where `username` = \'{username}\';
    '''

    # 将处理好的数据使用全局查询获取返回值给[data]
    user_name = us.global_query(sql)

    # 验证基本登录信息-数据校验
    # (True  -> 返回状态码: 404, 错误信息: 该用户不存在！
    # (False -> 返回解析值 username 为 username:type > tuple[0][0]
    if not user_name:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '该用户不存在！'
        return return_value
    else:
        username = user_name[0][0]

    # 拼接SQL > 判断sql_1末尾是不是';'如果是则去掉
    if info[-1] == ';':
        info = info[:-1]

    # 数据库查询语句B
    # 使用SQL > 根据username和password来获取数据
    sql = f'''
    {info} where `username` = \'{username}\' and `password` = \'{password}\';
    '''

    # 将处理好的数据使用全局查询获取返回值给[data]
    user_info = us.global_query(sql)

    # 验证基本登录信息-数据校验
    # (True  -> 返回状态码: 404, 错误信息: 密码错误！
    # (False -> 返回解析值 username 为 username:type > tuple[0] & 删除['msg']['error_msg']键值对
    if not user_info:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '密码错误！'
        return return_value
    else:
        user_info = user_info[0]
        del return_value['msg']['error_msg']

    # 将数据库中的字段与data['msg']的key进行对比，如果相同，则将数据库中的字段值赋值给data['msg']的key
    for key in return_value['msg'].keys():
        if key in fields:
            return_value['msg'][key] = user_info[fields.index(key)]

    # WARNING：设计问题，手动获取user_id ( 可能会出现问题 )
    return_value['msg']['user_id'] = user_info[0]

    # 根据时间戳生成token
    return_value['msg']['token'] = uo.create_token()

    # 根据user_id更新token(时间戳)
    update_sql = f'update {st.TABLE_人员表} set token = \'{uo.create_token()}\' where id = {user_info[0]}'
    us.global_modify(update_sql)

    # 返回处理后的数据-对接接口
    return return_value


def register_check(name, username, password, job):
    """ 注册检查 """
    return_value = {
        'status_code': 200,
        'msg': {
            'error_msg': "",
        }
    }

    if not name:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '姓名不能为空'
        return return_value
    if not username:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '邮箱不能为空'
        return return_value
    if not password:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '密码不能为空'
        return return_value
    if not job:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '职位不能为空'
        return return_value

    if job == '系主任':
        insert_sql = f'''
        insert into {st.TABLE_人员表}(`name`,`username`,`password`,`is_headdepart`) values('{name}','{username}','{password}',1);
        '''
    elif job == '班主任':
        insert_sql = f'''
        insert into {st.TABLE_人员表}(`name`,`username`,`password`,`is_headteacher`) values('{name}','{username}','{password}',1);
        '''
    elif job == '督察员':
        insert_sql = f'''
        insert into {st.TABLE_人员表}(`name`,`username`,`password`,`is_inspector`) values('{name}','{username}','{password}',1);
        '''
    else:
        insert_sql = f'''
        insert into {st.TABLE_人员表}(`name`,`username`,`password`,`is_inspector`,`is_headteacher`) values('{name}','{username}','{password}',1,1);
        '''

    res = us.global_modify(insert_sql)
    if isinstance(res, str) and 'Duplicate entry' in res:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '此邮箱以被注册！'

    return return_value


def class_check(username, password):
    # 构建[return_value]用于返回数据
    return_value = {
        'status_code': 200,  # 状态码
        'msg': {
            'error_msg': '',  # 错误信息
            'id': '',  # 学科编号
            'cls': '',  # 所在班级
            'classroom': '',  # 教室量化
            'dormitory': '',  # 宿舍量化
            'personal': '',  # 个人量化
            'floor': '',  # 楼道量化
            'discipline': '',  # 纪律
            'bzr': '',  # 获取 `user` 表对于的班主任
            'jcy': '',  # 获取 `user` 表对于的检察员
            'inspect_time': ''  # 记录 `time` 对于检查的时间
        }
    }

    # 验证基本登录信息-数据校验
    if not username or not password:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '用户名或密码为空！'
        return return_value

    return_infos = uj.user_res(username, password)

    if return_infos['status_code'] == 404:
        return_value['status_code'] = 404
        return_value['msg']['error_msg'] = '数据状态异常！'
        return return_value
    else:
        return_value = return_value['msg']
        return_infos = return_infos['msg']
        del return_value['error_msg']

    # 调用构建字典接口-数据处理
    return_value = dp.build_dict(return_value, return_infos)

    # 数据处理
    # (1 将['return_value']['bzr']中班主任的名字append(追加)到bar_name_list中
    # 使用 SQL select `name` from {st.TABLE_人员表} where `id` in () 语句查询获取 `name` 对应的 `id` 字段 > 用于后续匹配
    # 例如 ['demo', 'xxx', 'xxx', 'xxx']
    bzr_us_sql = ''
    bzr_us_len = len(return_value)

    if bzr_us_len <= 1:
        bzr_us_sql = f'''= {[i['bzr'] for i in return_value][0]}'''

    if bzr_us_len >= 2:
        bzr_us_sql = f'''in {tuple([i['bzr'] for i in return_value])}'''

    # 数据格式转换 tuple -> dict (('1', '邢予'), ('2', '吴洁'), ('8', 'demo'))转换为 {1: '邢予', 2: '吴洁', 8: 'dome'}

    bzr_id_dict = {i[0]: i[1] for i in us.global_query(
        f'''
        select distinct `id`, `name` from {st.TABLE_人员表} where `id` {bzr_us_sql}
        '''
    )}

    # 数据处理
    # (1 将['return_value']['bzr']中班主任的名字append(追加)到bar_name_list中
    # 使用 SQL select `name` from {st.TABLE_人员表} where `id` in () 语句查询获取 `name` 对应的 `id` 字段 > 用于后续匹配
    # 例如 ['demo', 'xxx', 'xxx', 'xxx']
    jcy_us_sql = ''
    jcy_us_len = len(return_value)

    if jcy_us_len <= 1:
        jcy_us_sql = f'''= {[i['jcy'] for i in return_value][0]}'''

    if bzr_us_len >= 2:
        jcy_us_sql = f'''in {tuple([i['jcy'] for i in return_value])}'''

    # 数据格式转换 tuple -> dict (('1', '邢予'), ('2', '吴洁'), ('8', 'demo'))转换为 {1: '邢予', 2: '吴洁', 8: 'dome'}

    jcy_id_dict = {i[0]: i[1] for i in us.global_query(
        f'''
            select distinct `id`, `name` from {st.TABLE_人员表} where `id` {jcy_us_sql}
            '''
    )}

    # (2 将['return_value']['bzr']中班主任的id替换为对应的名字
    # 例如 ['邢予', 'xxx', 'xxx', 'xxx']

    for i in return_value:
        try:
            i['bzr'] = bzr_id_dict[i['bzr']]
        except KeyError:
            i['bzr'] = bzr_id_dict[str(i['bzr'])]

    # (3 将['return_value']['bzr']中检察院的id替换为对应的名字
    # 例如 ['邢予', 'xxx', 'xxx', 'xxx']
    for i in return_value:
        try:
            i['jcy'] = jcy_id_dict[i['jcy']]
        except KeyError:
            i['jcy'] = jcy_id_dict[str(i['jcy'])]

    # 将['return_value']['bzr']中班主任的id替换为对应的名字

    return_infos = us.rule_query(
        st.TABLE_检查结果表, ['create_time', 'update_time'], True, False
    )

    no_dict = dp.build_field(return_infos)

    # 将no_dict 中 user_id 换成 bzr
    no_dict[no_dict.index('inspector_id')] = 'jcy'
    no_dict[no_dict.index('user_id')] = 'bzr'
    fields = dp.build_index(no_dict, 'cls', 'bzr')
    # fields = dp.build_index(no_dict, 'cls', 'jcy')

    # todo inspect_items 值！
    # print(fields, '\n', '--' * 20)

    loc = locals()

    res = {
        'data_info': return_value.copy()
    }

    res['length'] = [len(res['data_info'])]

    for f in fields:
        loc[f] = [json.loads(i[k]) for i in return_value for k, v in i.items() if
                  k not in no_dict[:3] + [f] + no_dict[5:]]
        res[f] = loc[f]

    # data = [json.loads(i[k]) for i in return_value.copy() for k, v in i.items() if k not in no_dict]

    # [j.update({'score': j.pop('分数'), 'reduce': dict(
    #     zip(['k' + str(k) for k in range(1, len(j['减分项']) + 1)], j.pop('减分项').values())
    # )}) for i in fields for j in res[i]]

    data_list = [
        {
            k: i[k] for k in ['id', 'cls', 'bzr', 'jcy', 'inspect_time'] if k in i
        } | {
            'inspect_items': {
                k: ast.literal_eval(v) for k, v in i.items() if k in fields
            }
        } for i in res['data_info']
    ]

    # data_list = []
    # for i in res['data_info']:
    #     each_data = {}
    #     inspect_items = {}
    #     for k, v in i.items():
    #         try:
    #             inspect_items[k] = ast.literal_eval(v)
    #         except Exception as e:
    #             each_data[k] = v
    #     each_data['inspect_items'] = inspect_items
    #     data_list.append(each_data)
    #
    return_value = data_list.copy()

    # del res['data_info']

    # print(res, '\n', '--' * 20)

    return return_value


def inspect_info_check(user_value):
    """
    It receives the response from the server.
    """

    """
    接收检查结果，并保存数据库
    接收的数据举例：// 目前的“minus_projects”项为临时模拟数据
        {
            'inspector':{       //  检查员
                'name':'王璐',   // 姓名
                'token':'91f6a0670e74ae6acb8cc6e72738d19d', // token
            },
            'inspect_res':{     // 检查结果
                'score':40,     // 得分
                'minus_projects':{      // 扣分项
                    'sanitation':{      // 卫生
                    'confetti':10,      // 纸屑，扣10分
                    'blackboard':10,     // 黑板，扣10分
                    'WaterGlass':10,     // 水杯摆放，扣10分
                    },
                    'dormitory':{
                        'bend':10,        // 床，扣10分
                        'clothes':10,     // 衣服，扣10分
                        'ground':10,      // 地面，扣10分
                    },
                }
            }
        }
    """

    return_value = {
        'status_code': 200,  # 状态码 ,如果状态吗是404，请查看msg信息
        'msg': {
            'error_msg': '',  # 错误信息
            'success_msg': '',  # 成功信息
        },
        'inspector': {
            'username': '',  # 检查员姓名
            'token': '',  # 检查员token
        },
        'inspect_res': {
            'score': 100,  # 得分
            'minus_projects': {},  # 扣分项
        }
    }

    # 1. 检查检查员是否存在
    if not user_value:
        return_value['status_code'] = 404
        return_value['msg'] = 'data数据为空！需要传输json数据！'
        return return_value
    else:
        return_value['inspector']['username'] = user_value['username']
        return_value['inspector']['token'] = user_value['token']
        user_info = user_value['data']

    # print(f'k1 {user_info} \n {user_info.keys()} \n {"--" * 20}')

    if 'msg' and 'status_code' in user_info.keys():
        del user_info['msg']
        del user_info['status_code']

    # print(f'k1 {user_info} \n {user_info.keys()} \n {"--" * 20}')

    minus_projects = user_info['inspect_items']
    # list_translate = user_info['translate']

    return_value['inspect_res']['minus_projects'] = minus_projects

    # 检查token值是否匹配
    sql = f'''
        select `id` from {st.TABLE_人员表} 
        where `name`='{user_value['username']}' and `token`='{user_value['token']}'
        '''

    res = us.global_query(sql)
    if not res:
        return_value['msg'] = '数据已收到，但是Token值不匹配！'
        return return_value
    # else:
    #     return_value['msg'] = '数据接收成功!'

    # print(f'k {return_value} \n {"--" * 20}')

    # todo 数据存储

    q_type = return_value['inspect_res']['minus_projects']  # 量化类型 quantization type
    # q_type['classroom']

    # 便利q_type的所有value中int类型的值的
    for k, v in q_type.items():
        tmp_dict = {}
        q_scos = sum([i for i in v.values() if isinstance(i, int)])
        tmp_dict['分数'] = 100 - q_scos
        tmp_dict['减分项'] = v
        q_type[k] = str(tmp_dict).replace('\'', '"').replace(' ', '')

    # sum_score = sum([i['分数'] * 0.2 for i in q_type.values()])

    sql = f'''
            insert into {st.TABLE_检查结果表}(`cls`,`user_id`,`inspector_id`,`classroom`,`dormitory`,`personal`,`floor`,`discipline`)
            values('大数据20-1', 1, 2, '{q_type['classroom']}', '{q_type['dormitory']}', '{q_type['personal']}', '{q_type['floor']}', '{q_type['discipline']}')
             '''
    res = us.global_modify(sql)
    if res != -1:
        return_value['msg'] = '数据格式验证成功！'

    return return_value


def inspect_time_check(user_value):
    user_value = user_value.copy()
    user_value.copy()
    """
        获取所有需要检查的项目表数据
        # 接收的数据举例：
        #     {
        #         'name':'王璐',   // 姓名
        #         'token':'91f6a0670e74ae6acb8cc6e72738d19d', // token
        #     }
        返回值：
        {
            'status_code':200,
            'msg':"",  // 信息
            'inspect_items':{
                'classroom':{
                    '黑板':10,
                    '桌椅':10,
                    '水杯':10,
                    '其他':10,
                },
                'dormitory':{
                    '垃圾':10,
                    '衣物':10,
                    '其他':10,
                },
                ...
            },
        }
        """

    # table_comment_dict的缩写
    return_value = {
        'status_code': 200,
        'msg': '获取数据成功！',
        'inspect_items': {}
    }

    # # token验证
    # data = request.get_json()
    # # 判断data是否为空
    # if not data:
    #     return_value['msg'] = 'data数据为空！需要传输json数据！'
    #     return return_value

    # # data不为空，做如下处理
    # return_value['data'] = json.dumps(data)  # 先赋值

    # # 检查token值是否匹配
    # query_sql = f'''
    # select `id` from {st.TABLE_人员表}
    # where `name`='{data['name']}' and `token`='{data['token']}'
    # '''
    # res = us.global_query(query_sql)
    # if not res:
    #     return_value['msg'] = '数据已收到，但是Token值不匹配！'
    #     return return_value

    query_sql = f"""select category, item, score from {st.TABLE_检查项目表}"""
    res = us.global_query(query_sql)  # (('教室', '黑板', 10), ('教室', '桌椅', 10), ('教室', '水杯', 10))
    if not res:
        return_value['status_code'] = 404
        return_value['msg'] = '获取数据失败！没有查询到检查项数据！'

    inspect_items = {}
    for r in res:
        inspect_items[r[0]] = {}
    for r in res:
        inspect_items[r[0]][r[1]] = r[2]
    return_value['inspect_items'] = inspect_items
    return_value['translate'] = ['教室', '纪律', '宿舍', '楼值', '个人卫生']
    return return_value


if __name__ == '__main__':
    import time

    t = time.time()
    print('func start', '\n', '--' * 20)
    # class_check('demo@qq.com', 'demo')
    class_check('wujie@qq.com', 'wujie321')
    # class_check('wanglu@qq.com', 'wanglu321')
    print('func end', '\n', '--' * 20)
    print(f'coast:{time.time() - t:.8f}s')
