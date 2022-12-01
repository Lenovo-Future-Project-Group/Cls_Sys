import ast

inspect_res_list = [
    {'id': 3, 'cls': '大数据201', 'classroom': '{"分数":80,"减分项":{"纸屑":10,"黑板":10}}',
     'dormitory': '{"分数":80,"减分项":{"床铺":10,"衣物叠放":10}}',
     'personal': '{"分数":80,"减分项":{"指甲":10,"头发":10}}', 'floor': '{"分数":80,"减分项":{"地面":10,"垃圾桶":10}}',
     'discipline': '{"分数":80,"减分项":{"上课打闹":10,"玩手机":10}}', 'bzr': 'demo', 'inspect_time': 4},
    {'id': 5, 'cls': '大数据201', 'classroom': '{"分数":80,"减分项":{"纸屑":10,"黑板":10}}',
     'dormitory': '{"分数":80,"减分项":{"床铺":10,"衣物叠放":10}}',
     'personal': '{"分数":80,"减分项":{"指甲":10,"头发":10}}', 'floor': '{"分数":80,"减分项":{"地面":10,"垃圾桶":10}}',
     'discipline': '{"分数":80,"减分项":{"上课打闹":10,"玩手机":10}}', 'bzr': 'demo', 'inspect_time': 6}
]
data_list = []
for i in inspect_res_list:
    each_data = {}
    inspect_items = {}
    for k, v in i.items():
        try:
            inspect_items[k] = ast.literal_eval(v)
        except Exception as e:
            print(e)
            each_data[k] = v
    each_data['inspect_items'] = inspect_items
    data_list.append(each_data)
print(data_list)
