# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 17:25
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : header.py
# @Software: PyCharm
"""

from  utils.generator import *
from utils.base import interface_no
import time
import json

class Header(object):
    
   
   def request_header(self):
       '''请求报文报文头'''
       header  = {}
       header['version'] = '1.0.0'
       header['tradeType'] = '00'
       header['merchantNo'] = '131010000011003'
       header['tradeDate'] = time.strftime("%Y%m%d", time.localtime())
       header['tradeTime'] = time.strftime("%H%H%S", time.localtime())
       header['merOrderNo'] = random_str(1, 10)
       header['tradeCode'] = interface_no.number.get('cg1001')
       
       return header
    
    
    
if __name__ == '__main__':
    h = Header().request_header()
    print(h)