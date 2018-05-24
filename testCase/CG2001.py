# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/24 17:46
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : CG2001.py
# @Software: PyCharm
"""
import json
import unittest
import requests
from utils.base.generator import *
from testData.Interface.header import Header
from utils.configAssertion import assertHTTPCode
from utils.configBase import Config
from utils.configHttp import HTTPClient
from utils.log import logger


class TestCG2001(unittest.TestCase):
    '''
    TestCG1001测试类
    '''
    merOrderNo = random_str(5, 10)
    merchantNo = '131010000011003'
    tradeDate = time.strftime("%Y%m%d", time.localtime())
    tradeTime = time.strftime("%H%M%S", time.localtime())
    tradeCode = 'CG2001'
    
    acctNo = "13101000001100304"
    
    cg2001_json = {
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
            "acctNo": acctNo
        }
    }
    
    interface_url = Config().get('cg2001')
    http_header = Header().headers
    request_string = json.dumps(cg2001_json)
    
    
    def setUp(self):
        url1 = "http://localhost:8080/run_sign"
        url2 = "http://localhost:8080/run_des_pkcs5"
        url3 = "http://localhost:8080/run_rsa_pkcs1"
        key = "12345678"
        headers = {
            "host": "127.0.0.1",
            "Content-Type": "application/json",
            "connection": "Keep-Alive",
            "accept-encoding": "gzip, deflate"
        }
        data_test1 = {
            "unsign_request": self.request_string
        }
        data_test2 = {
            "unencrypted_request": self.request_string
        }
        data_test3 = {
            "unencrypted_key": key
        }

        response1 = requests.post(url1, data=json.dumps(data_test1), headers=headers)
        response2 = requests.post(url2, data=json.dumps(data_test2), headers=headers)
        response3 = requests.post(url3, data=json.dumps(data_test3), headers=headers)
        sign = response1.text
        print(sign + "\n")
        jsonEnc = response2.text
        print(jsonEnc + "\n")
        keyEnc = response3.text
        print(keyEnc + "\n")
        
        self.client = HTTPClient(
            url=self.interface_url,
            method='POST',
            timeout=10,
            headers=self.http_header)
        self.data = {
            "sign": sign,
            "jsonEnc": jsonEnc,
            "keyEnc": keyEnc,
            "merchantNo": self.merchantNo,
            "merOrderNo": self.merOrderNo
        }
    
    def test_cg2001(self):
        try:
            res = self.client.send(data=json.dumps(self.data))
            print(res.status_code)
            logger.error(res.text)
            assertHTTPCode(res, [200])
            self.assertEquals(200, res.status_code)
        except requests.exceptions.ConnectTimeout:
            raise TimeoutError
    


if __name__ == '__main__':
    unittest.main()