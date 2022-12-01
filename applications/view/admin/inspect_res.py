from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user

from applications.models.quantify import user_check_tools as uc

admin_inspect_res = Blueprint('adminInspectRes', __name__, url_prefix='/admin/inspect_res')


# 督查数据管理
@admin_inspect_res.get('/')
# @authorize("admin:user:main", log=True)
def main():
    username = current_user.username
    password = current_user.password_hash

    datalist = uc.class_check(username, password)

    # inspect_res_list = [{'id': 3, 'cls': '大数据201', 'bzr': '吴洁', 'inspect_time': 4, 'inspect_items': {'classroom': {'分数': 80, '减分项': {'纸屑': 10, '黑板': 10}}, 'dormitory': {'分数': 80, '减分项': {'床铺': 10, '衣物叠放': 10}}, 'personal': {'分数': 80, '减分项': {'指甲': 10, '头发': 10}}, 'floor': {'分数': 80, '减分项': {'地面': 10, '垃圾桶': 10}}, 'discipline': {'分数': 80, '减分项': {'上课打闹': 10, '玩手机': 10}}}}]

    # return inspect_res_list
    return render_template('admin/inspect_res/inspect_res.html', inspect_res_list=datalist)
    # return render_template('admin/inspect_res/test.html', inspect_res_list=inspect_res_list)

#   用户分页查询
# @admin_inspect_res.get('/data')
# @admin_inspect_res("admin:user:main", log=True)
# def data():
#     # 获取请求参数
#     real_name = xss_escape(request.args.get('realName', type=str))
#     username = xss_escape(request.args.get('username', type=str))
#     dept_id = request.args.get('deptId', type=int)
#     # 查询参数构造
#     mf = ModelFilter()
#     if real_name:
#         mf.contains(field_name="realname", value=real_name)
#     if username:
#         mf.contains(field_name="username", value=username)
#     if dept_id:
#         mf.exact(field_name="dept_id", value=dept_id)
#     # orm查询
#     # 使用分页获取data需要.items
#     user = User.query.filter(mf.get_filter(model=User)).layui_paginate()
#     count = user.total
#     # 返回api
#     return table_api(data=model_to_dicts(schema=UserOutSchema, data=user.items), count=count)


# #  编辑用户
# @admin_user.get('/edit/<int:id>')
# def edit(id):
#     return render_template('admin/user/edit.html', user=user, roles=roles, checked_roles=checked_roles)


# #  编辑用户
# @admin_user.put('/update')
# def update():
#     return success_api(msg="更新成功")


# # 删除用户
# @admin_user.delete('/remove/<int:id>')
# @authorize("admin:user:remove", log=True)
# def delete(id):
#     user = User.query.filter_by(id=id).first()
#     user.role = []

#     res = User.query.filter_by(id=id).delete()
#     db.session.commit()
#     if not res:
#         return fail_api(msg="删除失败")
#     return success_api(msg="删除成功")


# # 批量删除
# @admin_user.delete('/batchRemove')
# def batch_remove():
#     return success_api(msg="批量删除成功")
