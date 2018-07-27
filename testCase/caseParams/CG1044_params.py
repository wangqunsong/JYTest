# -*- coding: utf-8 -*-
"""
# @Time    : 2018/7/23 10:41
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : CG1044_params.py
# @Software: PyCharm
"""
from utils.base.generator import random_phone_number
from utils.base.generator import random_cardNo
from utils.base.generator import random_name
from utils.base.generator import random_email
'''
  GC1044接口参数
'''

# 回调通知地址
callbackUrl = "http://10.10.10.185:9101/depositDemo/merchant/notify.do"
# 跳转地址
responsePath = "https://www.baidu.com"
# 请求版本
version = "1.0.0"
# 报文类型:00请求报文   01响应报文
tradeType = "00"
# 商户号
merchantNo = "131010000011003"


cg1044 = (
    {"caseName": "注册成功_投资人",
     "registerPhone": random_phone_number,
     "custType": "00",
     "callbackUrl": callbackUrl,
     "responsePath": responsePath,
     "cardNo": random_cardNo,
     "code": "485125",
     "name": random_name,
     "phone": random_phone_number,
     "mailAddr": random_email
     },
    {
        "caseName": "注册成功_融资人",
        "registerPhone": random_phone_number,
        "custType": "03",
        "callbackUrl": callbackUrl,
        "responsePath": responsePath,
        "cardNo": random_cardNo,
        "code": "485125",
        "name": random_name,
        "phone": random_phone_number,
        "mailAddr": random_email
    },
)
