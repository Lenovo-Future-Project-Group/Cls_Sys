# 班级量化管理系统

## 一、接口说明文档
### 1. 登陆验证接口
- 请求方式：POST
- 参数：username、password、ptype
    - 说明：
        - username：用户名
        - password：密码
    - 举例：
        - 吴洁需要登陆：
        `username="吴洁",password="wujie321"`
        
- 返回结果
    - 正确请求：
        ```
        {   "status_code":200,
            "msg":{
                "error_msg":"",
                "token":"token值",
                "id":"id值",
                "name":"姓名",
                "is_headdepart":"是否系主任，1是，0否",
                "is_inspector":"是否检查员，1是，0否",
                "is_headteacher":"是否班主任，1是，0否",
                "permission_level":"权限等级，1~4级，4级最高",
            }
        }
        ```
    - 错误请求：
        - **参数错误**（即"username"或"password"这两个单词拼写错误，或者它们对应的值为空）：
        ```
        {   "status_code":200,
            "msg":{
                "error_msg":"用户名或密码为空！",
                "token":"",
                "id":"",
                "name":"",
                "is_headdepart":"",
                "is_inspector":"",
                "is_headteacher":"",
                "permission_level":"",
            }
        }
        ```
        - **用户名或密码错误**：
        ```
        {   "status_code":200,
            "msg":{
                "error_msg":"用户名或密码有误！",
                "token":"",
                "id":"",
                "name":"",
                "is_headdepart":"",
                "is_inspector":"",
                "is_headteacher":"",
                "permission_level":"",
            }
        }
        ```
- 举例如图：
    - 正确访问：
    ![](https://tva1.sinaimg.cn/large/008vxvgGly1h7da0dmccjj31bx0u0wj4.jpg)
    - 参数错误：
    ![](https://tva1.sinaimg.cn/large/008vxvgGly1h7da0dfylyj31b00u0aew.jpg)
    - 用户名或密码错误
    ![](https://tva1.sinaimg.cn/large/008vxvgGly1h7da0d7zi7j31av0u0q7h.jpg)