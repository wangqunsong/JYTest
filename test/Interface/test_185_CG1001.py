# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 17:03
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : test_185_CG1001.py
# @Software: PyCharm
"""

import json
import unittest
from data.Interface.header import Header
from data.Interface.cg1001_body import Body_CG1001
from utils.assertion import assertHTTPCode
from utils.client import HTTPClient
from utils.config import Config
from utils.log import logger


class TestCG1001(unittest.TestCase):
    interface_url = Config().get('cg1001')
    headers = Header().request_header()
    body = Body_CG1001().request_body_cg1001()
    
    def setUp(self):
        self.client = HTTPClient()
        self.client.set_data(self.body)
        self.client.set_url(self.interface_url)
        self.client.set_headers(self.headers)
    
    def test_cg1001(self):
        
        res = self.client.post(url=self.interface_url, headers=json.dumps(self.headers), data=json.dumps(self.body))
        print(res.text)
        logger.error(res.text)
        assertHTTPCode(res, [000000])
        self.assertIn('000000', res.text)
        
if __name__ == '__main__':
    test = TestCG1001()
    test.test_cg1001()
