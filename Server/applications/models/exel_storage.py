from IPython.core.display_functions import display
from applications.common import setting as st
from applications.models import user_check_tools as uc, sql_data_tools as us, data_processing_tools as dp
import pandas as pd


def index():
    return_infos = us.rule_query(
        st.TABLE_检查结果表, ['create_time', 'update_time'], True, False
    )

    no_dict = dp.build_field(return_infos)

    # 将no_dict 中 user_id 换成 bzr

    no_dict[no_dict.index('user_id')] = 'bzr'
    fields_main = dp.build_index(no_dict, 'cls', 'bzr')
    fields_scos = ['分数', '减分项']

    # sql = us.rule_query(
    #     st.TABLE_人员表, ['username', 'password'], False, True
    # )

    res = uc.class_check('wujie@qq.com', 'wujie321')

    res = pd.DataFrame.from_dict(res.copy())

    for i in fields_main:
        res[i] = res['inspect_items'].map(lambda x: x[i])
        for j in fields_scos:
            res[j] = res['classroom'].map(lambda x: x[j])

    return res

    # user_info_dict = {i[0]: i[1] for i in us.global_query(sql)}

    # for k, v in user_info_dict.items():
    #     res = uc.class_check(k, v)
    #     print(res)


if __name__ == '__main__':
    import time

    t = time.time()
    print('func start', '\n', '--' * 20)
    test = index()
    display(test)
    print('func end', '\n', '--' * 20)
    print(f'coast:{time.time() - t:.8f}s')
