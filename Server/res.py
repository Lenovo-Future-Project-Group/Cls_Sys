user_data = {'data_info': [{'id': 3, 'cls': '大数据201', 'classroom': '{"分数":80, "减分项":{"纸屑":10, "黑板":10}}',
                            'dormitory': '{"分数":80, "减分项":{"床铺":10, "衣物叠放":10}}',
                            'personal': '{"分数":80, "减分项":{"指甲":10, "头发":10}}',
                            'floor': '{"分数":80, "减分项":{"地面":10, "垃圾桶":10}}',
                            'discipline': '{"分数":80, "减分项":{"上课打闹":10, "玩手机":10}}', 'bzr': '吴洁',
                            'inspect_time': 4}], 'classroom': [{'分数': 80, '减分项': {'床铺': 10, '衣物叠放': 10}},
                                                               {'分数': 80, '减分项': {'指甲': 10, '头发': 10}}],
             'dormitory': [{'分数': 80, '减分项': {'指甲': 10, '头发': 10}}],
             'personal': [{'分数': 80, '减分项': {'床铺': 10, '衣物叠放': 10}}],
             'floor': [{'分数': 80, '减分项': {'床铺': 10, '衣物叠放': 10}},
                       {'分数': 80, '减分项': {'指甲': 10, '头发': 10}}],
             'discipline': [{'分数': 80, '减分项': {'床铺': 10, '衣物叠放': 10}},
                            {'分数': 80, '减分项': {'指甲': 10, '头发': 10}}]}

user_info = ['classroom', 'dormitory', 'personal', 'floor', 'discipline']


def index():
    [j.update({'score': j.pop('分数'), 'reduce': dict(
        zip(['k' + str(k) for k in range(1, len(j['减分项']) + 1)][0], j.pop('减分项').values())
    )}) for i in user_info for j in user_data[i]]

    user_data['length'] = len(user_data['data_info'])

    # 去除里面的列表

    return user_data


if __name__ == '__main__':
    print(index())
