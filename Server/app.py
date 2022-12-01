from flask import Flask, request, url_for, redirect, render_template, session, make_response, jsonify
from flask_session import Session
from flask_cors import CORS

from applications.models import user_check_tools as uc

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# 添加跨域请求允许的头部字段
# 对当前这个flask 核心对象app添加access-control-origin的头部字段
# 对/下所有的url 允许所有的origins来访问
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/index/', methods=['GET', 'POST'])
def index():
    if not session.get('username') and not session.get('password'):
        return redirect(url_for('login'))

    username = session.get('username')
    password = session.get('password')

    data_list = uc.index_check(username, password)['user_data']

    return render_template('index.html', inspect_res_list=data_list)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']

    username = session.get('username')
    password = session.get('password')

    return_value = uc.login_check(username, password)
    # 设置响应请求头
    response = make_response(jsonify(return_value))
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
    response.headers['Access-Control-Allow-Methods'] = 'POST'  # 允许的请求方法
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  # 允许的请求header
    return response


@app.route('/register', methods=['POST'])
def register():
    """ 注册功能 """
    name = request.form.get('name')
    username = request.form.get('email')  # 邮箱
    password = request.form.get('password')
    job = request.form.get('job')  # 职位
    return uc.register_check(name, username, password, job)


@app.route('/login_inspector/', methods=['POST'])
def login_inspector():
    """ 检查员登陆 """
    username = request.form.get('username')
    password = request.form.get('password')

    return_value = uc.login_check(username, password)
    # 设置响应请求头
    response = make_response(jsonify(return_value))
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
    response.headers['Access-Control-Allow-Methods'] = 'POST'  # 允许的请求方法
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  # 允许的请求header
    return response


@app.route('/logout')
def logout():
    session['username'] = None
    session['password'] = None
    return redirect('/')


@app.route('/receive_inspect_res/', methods=['GET', 'POST'])
def receive_res():
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
    # 设置返回值
    return_value = {
        'status_code': 200,  # 状态码 ,如果状态吗是404，请查看msg信息
        'msg': '',
        'data': ''
    }

    if request.method == 'GET':
        return_value['status_code'] = 404
        return_value['msg'] = '请使用POST请求！'
        return return_value

    return_value = request.get_json()

    return_value = uc.inspect_info_check(return_value)

    # 判断里面是否有data
    if return_value.get('data'):
        return_value = return_value['data']
    else:
        return_value = return_value

    # 设置响应请求头
    response = make_response(jsonify(return_value))
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
    response.headers['Access-Control-Allow-Methods'] = 'POST'  # 允许的请求方法
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  # 允许的请求header
    return response


@app.route('/all_inspecte_item', methods=['GET', 'POST'])
def all_inspecte_item():
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
    return_value = {
        'status_code': 200,  # 状态码 ,如果状态吗是404，请查看msg信息
        'msg': '',
        'data': ''
    }

    if request.method == 'GET':
        return_value['status_code'] = 404
        return_value['msg'] = '请使用POST请求！'
        return return_value

    return_value = uc.inspect_time_check(return_value)

    # 设置响应请求头
    response = make_response(jsonify(return_value))
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许使用响应数据的域。也可以利用请求header中的host字段做一个过滤器。
    response.headers['Access-Control-Allow-Methods'] = 'POST'  # 允许的请求方法
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  # 允许的请求header
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4321, debug=True)
