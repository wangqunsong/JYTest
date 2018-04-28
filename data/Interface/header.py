# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 17:25
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : header.py
# @Software: PyCharm
"""

import time

from data.Interface import interface_no
from utils.generator import *


class Header(object):

    def request_header(self):
        '''请求报文报文头'''
        merchantNo_value = '131010000011003'
        merOrderNo_value = random_str(5, 10)
        tradeCode_value = interface_no.interface_number.get('cg1001')
        tradeDate_value = time.strftime("%Y%m%d", time.localtime())
        tradeTime_value = time.strftime("%H%H%S", time.localtime())
        header = dict(
            version='1.0.0',
            tradeType='00',
            merchantNo=merchantNo_value,
            tradeDate=tradeDate_value,
            tradeTime=tradeTime_value,
            merOrderNo=merOrderNo_value,
            tradeCode=tradeCode_value)
        return header


if __name__ == '__main__':
    h = Header().request_header()
    print(h)
