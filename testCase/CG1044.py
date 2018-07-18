#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/7/18 15:08
# @python  : python3.5
# @Email   : wangqunsong@hotmail.com
# @File    : CG1044.py
# @Software: PyCharm


import json
import unittest
import paramunittest
import requests
from utils.base.generator import *
from utils.configBase import Config
from utils.configExcel import ConfigExcel
from utils.configHttp import HTTPClient
from utils.configHttpHeader import Header
from utils.log import logger

excel_cg1044 = ConfigExcel().get_xls_row("caselist.xlsx", "CG1044")


@paramunittest.parametrized(*excel_cg1044)
class TestCG1044(unittest.TestCase):
    '''
    TestCG1044测试类
    '''

    def setParameters(
            self,
            case_name,
            merchant_no,
            trade_code,
            query_flow,
            trade_code_body,
            flow_type,
            resp_code,
            resp_desc,
            result_code,
            result_msg):
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
        self.queryFlow = str(query_flow)
        self.flowType = str(flow_type)
        self.tradeCode_body = str(trade_code_body)
        self.respCode = str(resp_code)
        self.respDesc = str(resp_desc)
        self.resultCode = str(result_code)
        self.resultMsg = str(result_msg)
        self.response = None

    def setUp(self):
        self.interface_url = Config().get('cg1044')
        self.sign_encrypt_url = "http://192.168.20.128:8080/sign_and_encrypt"
        self.decrypt_and_verify_url = "http://192.168.20.128:8080/decrypt_and_verify"
        self.encrypt_headers = Header.encrypt_decrypt_headers
        self.http_header = Header().request_headers
        self.merOrderNo = random_str(5, 10)
        self.tradeDate = time.strftime("%Y%m%d", time.localtime())
        self.tradeTime = time.strftime("%H%M%S", time.localtime())
        cg2002_json = {
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
                "tradeCode": self.tradeCode_body,
                "queryFlow": self.queryFlow,
                "flowType": self.flowType
            }
        }

        # 加密
        self.request_string = json.dumps(cg2002_json)
        self.sign_and_encrypt_data = {
            "unencrypt_string": self.request_string
        }
        sign_and_encrypt_response = requests.post(
            self.sign_encrypt_url, data=json.dumps(
                self.sign_and_encrypt_data), headers=self.encrypt_headers)
        sign_and_encrypt_response_txt = json.loads(
            sign_and_encrypt_response.text)
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
        #解密和验签
        try:
            request_response = self.client.send(data=json.dumps(self.data))
            request_response_txt = json.loads(request_response.text)
            self.decrypt_and_verify_data = {
                "sign": request_response_txt['sign'],
                "jsonEnc": request_response_txt['jsonEnc'],
                "keyEnc": request_response_txt['keyEnc']
            }
            self.decrypt_and_verify_response = requests.post(
                self.decrypt_and_verify_url, data=json.dumps(
                    self.decrypt_and_verify_data), headers=self.encrypt_headers)
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
        self.check2 = json.dumps(self.check['body'])
        self.check3 = json.loads(self.check2)

        logger.error(self.decrypt_and_verify_response.text)
        self.assertEqual(self.check3['resultCode'], self.resultCode)
        print("查询成功，开户结果为：" + self.check3['resultMsg'])
        print("查询的响应报文为：")
        print(self.check)


if __name__ == '__main__':
    unittest.main()