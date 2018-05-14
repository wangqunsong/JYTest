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
import paramunittest
import requests

from utils.base.DES import DesEncrypt
from utils.base.RSA import Sign
from utils.base.generator import *
from testData.Interface.header import Header
from utils.configAssertion import assertHTTPCode
from utils.configBase import Config
from utils.configHttp import HTTPClient
from utils.log import logger


# CG1001 = "cg1001"
# @paramunittest.parametrized(*CG1001)
class TestCG1001(unittest.TestCase):
    '''
    TestCG1001测试类
    '''
    merOrderNo = random_str(5, 10)
    merchantNo = '131010000011003'
    tradeDate = time.strftime("%Y%m%d", time.localtime())
    tradeTime = time.strftime("%H%M%S", time.localtime())
    tradeCode = 'CG1001'
    custName = random_name()
    mobile = random_phone_number()
    certType = "01"
    certNo = random_cerNO()
    payPassword = "111111"
    mailAddr = random_email()
    
    interface_url = Config().get('cg1001')
    http_header = Header().headers
    signRSA = Sign()
    desEncrypt = DesEncrypt()
    
    cg1001_json = {
        "head": {
            "version": "1.0.0",
            "tradeType": "00",
            "merchantNo": merchantNo,
            "tradeDate": tradeDate,
            "tradeTime": tradeTime,
            "merOrderNo": merOrderNo,
            "tradeCode": tradeCode
        },
        "body": {
            "custName": custName,
            "mobile": mobile,
            "certType": certType,  # 身份证
            "certNo": certNo,
            "payPassword": payPassword,
            "mailAddr": mailAddr
        }
    }
    sk = random_str(8, 8)
    sign = signRSA.sign_to_hex(signRSA.sign_string(json.dumps(cg1001_json)))
    jsonEnc = desEncrypt.des_to_hex(desEncrypt.des_encrypt(json.dumps(cg1001_json), sk))
    keyEnc = signRSA.sign_to_hex(signRSA.sign_string(sk))
    
    def setUp(self):
        self.client = HTTPClient(
            url=self.interface_url,
            method='POST',
            timeout=10,
            headers=self.http_header)
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
