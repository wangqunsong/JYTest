# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 15:31
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : test_baidu_http.py
# @Software: PyCharm
"""

import unittest
import requests
from utils.config import Config
from utils.client import HTTPClient
from utils.log import logger
from utils.assertion import assertHTTPCode


class TestBaiduHTTP(unittest.TestCase):
    
    def test_baidu_http(self):
        url = 'http://10.10.10.185:10003/services/cgbiz/cg1001'
        sign = '123456'
        jsonEnc = 'abcdedg'
        keyEnc = 'abcdedg'
        merOrder_no = 'abcdedg'
        res = requests.post(url=url, sign=sign, jsonEnc=jsonEnc, keyEnc=keyEnc,merOrder_no=merOrder_no)
        logger.debug(res.text)
    