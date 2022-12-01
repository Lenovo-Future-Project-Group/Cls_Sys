# 其他工具文件
import time
import hashlib


def create_token():
    """ 根据时间戳生成token """
    # 生成时间戳
    timestamp = time.time()
    # 生成MD5对象
    md5 = hashlib.md5()
    # 对数据加密
    md5.update(str(int(timestamp)).encode('utf-8'))
    # 获取密文
    pwd = md5.hexdigest()
    return pwd


if __name__ == '__main__':
    print(create_token())
