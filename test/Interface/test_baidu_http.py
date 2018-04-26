# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 15:31
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : test_baidu_http.py
# @Software: PyCharm
"""

import unittest
from utils.config import Config
from utils.client import HTTPClient
from utils.log import logger
from utils.assertion import assertHTTPCode


class TestBaiduHTTP(unittest.TestCase):
    target_url = Config().get('target_url')
    
    def setUp(self):
        self.client = HTTPClient(url=self.target_url, method='GET')
    
    def test_baidu_http(self):
        res = self.client.send()
        logger.debug(res.text)
        assertHTTPCode(res, [200])
        self.assertIn('百度一下，你就知道', res.text)
    