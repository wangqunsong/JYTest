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

import paramunittest
import requests
from utils.base.generator import *
from testData.Interface.header import Header
from utils.configBase import Config
from utils.configExcel import ConfigExcel
from utils.configHttp import HTTPClient
from utils.log import logger

excel_cg2001 = ConfigExcel().get_xls("case.xlsx", "CG2001")


@paramunittest.parametrized(*excel_cg2001)
class TestCG2001(unittest.TestCase):
    '''
    TestCG2001测试类
    '''
    
    def setParameters(self, case_name, merchant_no, trade_code, acctNo,resp_code,resp_desc):
        '''

        :param case_name:
        :param merchant_no:
        :param trade_code_header:
        :param flow_type:
        :param resp_code:
        :param resp_desc:
        :param result_code:
        :param result_msg_result_status:
        :return:
        '''
        self.caseName = str(case_name)
        self.merchantNo = str(merchant_no)
        self.tradeCode = str(trade_code)
        self.acctNo = str(acctNo)
        self.respCode = str(resp_code)
        self.respDesc = str(resp_desc)
        self.response = None
    
    def setUp(self):
        self.interface_url = Config().get('cg2001')
        self.sign_encrypt_url = "http://localhost:8080/sign_and_encrypt"
        self.decrypt_and_verify_url = "http://localhost:8080/decrypt_and_verify"
        self.encrypt_headers = Header.encrypt_decrypt_headers
        self.http_header = Header().request_headers
        self.merOrderNo = random_str(5, 10)
        self.tradeDate = time.strftime("%Y%m%d", time.localtime())
        self.tradeTime = time.strftime("%H%M%S", time.localtime())
        cg2001_json = {
            "head": {
                "version": "1.0.0",
                "tradeType": "00",
                "merchantNo": self.merchantNo,
                "tradeDate": self.tradeDate,
                "tradeTime": self.tradeTime,
                "merOrderNo": self.merOrderNo,
                "tradeCode": self.tradeCode
            },
            "body": {
                "acctNo": self.acctNo
            }
        }
        
        # 加密
        self.request_string = json.dumps(cg2001_json)
        self.sign_and_encrypt_data = {
            "unencrypt_string": self.request_string
        }
        sign_and_encrypt_response = requests.post(self.sign_encrypt_url, data=json.dumps(self.sign_and_encrypt_data),
                                                  headers=self.encrypt_headers)
        sign_and_encrypt_response_txt = json.loads(sign_and_encrypt_response.text)
        self.client = HTTPClient(
            url=self.interface_url,
            method='POST',
            timeout=10,
            headers=self.http_header)
        self.data = {
            "sign": sign_and_encrypt_response_txt['sign'],
            "jsonEnc": sign_and_encrypt_response_txt['jsonEnc'],
            "keyEnc": sign_and_encrypt_response_txt['keyEnc'],
            "merchantNo": self.merchantNo,
            "merOrderNo": self.merOrderNo
        }
    
    def test_cg2001(self):
        try:
            request_response = self.client.send(data=json.dumps(self.data))
            request_response_txt = json.loads(request_response.text)
            self.decrypt_and_verify_data = {
                "sign": request_response_txt['sign'],
                "jsonEnc": request_response_txt['jsonEnc'],
                "keyEnc": request_response_txt['keyEnc']
            }
            self.decrypt_and_verify_response = requests.post(self.decrypt_and_verify_url,
                                                             data=json.dumps(self.decrypt_and_verify_data),
                                                             headers=self.encrypt_headers)
            self.check_result()
        except requests.exceptions.ConnectTimeout:
            raise TimeoutError
    
    def tearDown(self):
        try:
            pass
        except requests.exceptions.ConnectTimeout:
            raise TimeoutError
    
    def check_result(self):
        self.result = json.loads(self.decrypt_and_verify_response.text)
        self.check = json.loads(self.result['json'])
        self.check2 = json.dumps(self.check['head'])
        self.check3 = json.loads(self.check2)
        
        logger.error(self.decrypt_and_verify_response.text)
        #self.assertEqual(self.check3['respCode'], self.respCode)
        print("余额查询成功，测试结果为：" + self.check3['respDesc'])
        print("余额查询响应报文为：")
        print(self.check)


if __name__ == '__main__':
    unittest.main()