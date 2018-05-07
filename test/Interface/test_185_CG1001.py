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
import requests
from data.Interface.cg1001_body import Body_CG1001
from utils.assertion import assertHTTPCode
from utils.client import HTTPClient
from utils.config import Config
from utils.log import logger
from data.Interface.header import Header
from utils.base.RSA import SHA1withRSA


class TestCG1001(unittest.TestCase):
    interface_url = Config().get('cg2002')
    headers = Header().headers
    body = Body_CG1001().body_cg1001
    merchantNo = Header.merchantNo_value
    merOrderNo = Header.merOrderNo_value

    def setUp(self):
        self.client = HTTPClient(
            url=self.interface_url,
            method='POST',
            timeout= 10,
            headers=self.headers)
        #self.sign = hex(SHA1withRSA.sign(json.dumps(self.json_cg1001)))
        self.sign = '123456'
        self.jsonEnc = 'abcdedg'
        self.keyEnc = 'abcdedg'
        self.merOrderNo = 'abcdedg'
        self.merchantNo = 'abcdedg'
        self.data = {
            "sign": self.sign,
            "jsonEnc": self.jsonEnc,
            "keyEnc": self.keyEnc,
            "merchantNo": self.merchantNo,
            "merOrderNo": self.merOrderNo
        }

    def test_cg1001(self):
        try:
            res = self.client.send(data=json.dumps(self.data))
            print(res.status_code)
            logger.error(res.text)
            assertHTTPCode(res, [200])
            self.assertIn('000000', res.text)
        except requests.exceptions.ConnectTimeout:
           raise TimeoutError


if __name__ == '__main__':
    unittest.main()
