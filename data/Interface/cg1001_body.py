# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/28 10:32
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : cg1001_body.py
# @Software: PyCharm
"""

from utils.generator import *


class Body_CG1001(object):

    def request_body_cg1001(self):
        '''cg1001接口请求报文体'''
        custName = random_name()
        mobile = random_phone_number()
        certType = '01'  # 身份证
        certNo = random_cerNO()
        payPassword = '111111'
        mailAddr = random_email()
        body_cg1001 = dict(
            custName=custName,
            mobile=mobile,
            certType=certType,
            certNo=certNo,
            payPassword=payPassword,
            mailAddr=mailAddr)
        return body_cg1001
