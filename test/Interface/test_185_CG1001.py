# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 17:03
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : test_185_CG1001.py
# @Software: PyCharm
"""

import unittest
from utils.config import Config
from utils.client import HTTPClient
from utils.log import logger
from utils.assertion import assertHTTPCode
from utils.base.header import Header
import json


class TestCG1001(unittest.TestCase):
    interface_url  = Config().get('cg1001')
    headers = json.dumps(Header().request_header(), ensure_ascii=False)
    
    def setUp(self):
        HTTPClient.set_headers(self.headers)
        self.client = HTTPClient(url=self.interface_url, method='POST', headers=self.headers)
    
    def test_cg1001(self):
        res = self.client.send()
        logger.debug(res.text)
        assertHTTPCode(res, [200])
        self.assertIn('s000000', res.text)
        
if __name__ == '__main__':
    test = TestCG1001()
    test.test_cg1001()
