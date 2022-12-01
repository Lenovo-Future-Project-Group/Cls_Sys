import json
import os


def images_read(path):
    """读取数据，验证数据状态"""
    try:
        with open(path, 'r+', encoding='utf-8', errors='ignore') as f:
            f.read()
    except ValueError:
        raise Exception('图像信息数据异常，请您核验一下。')


# todo 验证数据状态 需要完善

def images_path():
    """读取数据，判断文件路径"""
    try:
        images_read(os.path.abspath('.') + r'/static/images/hero-min.jpg')
        return os.path.abspath('.') + r'/static/'
    except FileNotFoundError:
        images_read(os.path.abspath('../..') + r'/static/images/hero-min.jpg')
        return os.path.abspath('../..') + r'/static/'


# todo 判断数据读取路径 需要完善

def images_info(type):
    """ 获取图片,cls类型是获取班级图片，否则获取学生图片 """
    if type == 'cla':
        folder = '/images/cls_imgs'
        return os.listdir(images_path() + folder)
    elif type == 'stu':
        stu_img_dict = {}
        folder = '/images/student_imgs'
        img = os.listdir(images_path() + folder)
        for i in img:
            name = i.split('.')[0]
            stu_img_dict[name] = i

        return stu_img_dict


# todo 学生图片信息 [stu] 需要完善


def images_info_introduction():
    """ 读取学生 """
    folder = 'students_introduction.json'
    with open(images_path() + folder, 'r', encoding='utf8') as f:
        content = json.load(f)

        return content


# todo 学生图片介绍 [stu] 需要完善

def images():
    data = \
        {
            'cla_images': images_info('cla'),
            'stu_images': images_info('stu'),
            'usa_iminfo': images_info_introduction(),
        }

    return data


# todo 数据信息汇总


if __name__ == '__main__':
    test = images()
    print(test)
