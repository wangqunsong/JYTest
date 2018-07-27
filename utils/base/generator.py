# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 16:43
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : generator.py
# @Software: PyCharm
"""

"""一些生成器方法，生成随机数，随机手机号，随机身份证号，以及连续数字等"""
import random
import time
from faker import Factory

fake = Factory().create('zh_CN')


def random_phone_number():
    '''随机手机号'''
    return fake.phone_number()


def random_name():
    """随机姓名"""
    return fake.name()

def random_cardNo():
    """随机民生银行借记卡"""
    return  "621691021219" + random.randint(0000,9999)


def random_address():
    """随机地址"""
    return fake.address()


def random_email():
    """随机email"""
    return fake.email()


def random_ipv4():
    """随机IPV4地址"""
    return fake.ipv4()


def random_str(min_chars=0, max_chars=8):
    """长度在最大值与最小值之间的随机字符串"""
    return fake.pystr(min_chars=min_chars, max_chars=max_chars)


def random_cerNO():
    """ 随机生成18位身份证号码 """
    ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
    t = time.localtime()[0]
    x = '%02d%02d%02d%04d%02d%02d%03d' % (
        random.randint(10, 99), random.randint(1, 99), random.randint(
            1, 99), random.randint(t - 80, t - 18),
        random.randint(1, 12), random.randint(1, 28), random.randint(1, 999))
    y = 0
    for i in range(17):
        y += int(x[i]) * ARR[i]
    cer_no = '%s%s' % (x, LAST[y % 11])
    return cer_no


def factory_generate_ids(starting_id=1, increment=1):
    """ 返回一个生成器函数，调用这个函数产生生成器，从starting_id开始，步长为increment。 """
    def generate_started_ids():
        val = starting_id
        local_increment = increment
        while True:
            yield val
            val += local_increment
    return generate_started_ids


def factory_choice_generator(values):
    """ 返回一个生成器函数，调用这个函数产生生成器，从给定的list中随机取一项。 """
    def choice_generator():
        my_list = list(values)
        # rand = random.Random()
        while True:
            yield random.choice(my_list)
    return choice_generator


if __name__ == '__main__':
    print(random_cerNO())
    print(random_str(8,8))
