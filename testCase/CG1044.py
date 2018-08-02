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
from testCase.caseParams.CG1044_params import *
from utils.base.generator import *
from utils.configBase import Config
#from utils.configExcel import ConfigExcel
from utils.configHttp import HTTPClient
from utils.configHttpHeader import Header
from utils.log import logger

#excel_cg1044 = ConfigExcel().get_xls_row("caselist.xlsx", "CG1044")
@paramunittest.parametrized(*cg1044)
class TestCG1044(unittest.TestCase):
    '''
    TestCG1044测试类
    '''

    def setParameters(
            self,
            caseName,
            merchantNo,
            tradeCode,
            registerPhone,
            custType,
            cardNo,
            code,
            name,
            phone,
            mailAddr,
            callbackUrl,
            responsePath,
            respCode):
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
        self.caseName = str(caseName)
        self.merchantNo = str(merchantNo)
        self.tradeCode = str(tradeCode)
        self.registerPhone = str(registerPhone)
        self.callbackUrl = str(callbackUrl)
        self.responsePath = str(responsePath)
        self.custType = str(custType)
        self.cardNo = str(cardNo)
        self.code = str(code)
        self.name = str(name)
        self.phone = str(phone)
        self.mailAddr = str(mailAddr)
        self.respCode = str(respCode)

    def setUp(self):
        self.interface_url = Config().get('cg1044')
        self.sign_encrypt_url = "http://192.168.20.128:8080/sign_and_encrypt"
        self.decrypt_and_verify_url = "http://192.168.20.128:8080/decrypt_and_verify"
        
        self.submit_url = "http://10.10.10.185:9008/dep-page-service/submit"
        self.submit_all_url = "http://10.10.10.185:9008/dep-page-service/submitAll"
        self.send_message_url = "http://10.10.10.185:9008/dep-page-service/sendSms?"
        
        
        self.encrypt_headers = Header.encrypt_decrypt_headers
        self.http_header = Header().request_headers_page
        self.merOrderNo = random_str(5, 10)
        self.tradeDate = time.strftime("%Y%m%d", time.localtime())
        self.tradeTime = time.strftime("%H%M%S", time.localtime())
        cg1044_json = {
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
                "registerPhone": self.registerPhone,
                "custType": self.custType,
                "callbackUrl": self.callbackUrl,
                "responsePath" : self.responsePath
            }
        }

        #签名和加密
        self.request_string = json.dumps(cg1044_json)
        self.sign_and_encrypt_data = {
            "unencrypt_string": self.request_string
        }
        sign_and_encrypt_response = requests.post(
            self.sign_encrypt_url, data=json.dumps(
                self.sign_and_encrypt_data), headers=self.encrypt_headers)
        sign_and_encrypt_response_txt = json.loads(
            sign_and_encrypt_response.text)
        
        #请求
        self.client = HTTPClient(
            url=self.interface_url,
            method='POST',
            timeout=10,
            headers=self.http_header)
        self.data = {
            "sign": sign_and_encrypt_response_txt['sign'],
            "jsonEnc": sign_and_encrypt_response_txt['jsonEnc'],
            "keyEnc": sign_and_encrypt_response_txt['keyEnc'],
            "merchantNo": self.merchantNo
           # "merOrderNo": self.merOrderNo
        }

    def test_cg1044(self):
        
        #请求返回的密文
        try:
            request_response = self.client.send(data=json.dumps(self.data))
            request_response_txt = json.loads(request_response.text)
            self.decrypt_and_verify_data = {
                "sign": request_response_txt['sign'],
                "jsonEnc": request_response_txt['jsonEnc'],
                "keyEnc": request_response_txt['keyEnc']
            }
            
            #获取cookie和token
            token = request_response.cookies.items()[0][1]
            cookies = request_response.cookies
            
            
            #获取验证码
            self.client = HTTPClient(
                url=self.send_message_url,
                method='POST',
                timeout=10,
                headers=self.http_header)
            self.data_message = {
                "phoneNo": self.phone,
                "token": token,
                "merchantNo": self.merchantNo
                # "merOrderNo": self.merOrderNo
            }

            request_response_message = self.client.send(data=json.dumps(self.data_message))
            message_token = request_response_message.cookies.items()[0][1]
            message_cookies = request_response_message.cookies
            
            #submit
            self.client = HTTPClient(
                url=self.submit_url,
                method='POST',
                timeout=10,
                headers=self.http_header)
            self.data_submit = {
                "cardNo": self.cardNo,
                "code": 485125,
                "idNo": self.idNo,
                "name" : self.name,
                "phone": self.phone,
                "smsCode": 485125,
                "mobile": self.registerPhone,
                "merchantNo" : self.merchantNo,
                "merOrderNo" : self.merOrderNo,
                "id": message_cookies,
                "token": message_token,
                "mailAddr": self.mailAddr
            }
            
            request_response_submit = self.client.send(data=json.dumps(self.data_submit))
            submit_token = request_response_submit.cookies.items()[0][1]
            submit_cookies = request_response_submit.cookies
            
            
            #submitAll
            self.client = HTTPClient(
                url=self.submit_all_url,
                method='POST',
                timeout=10,
                headers=self.http_header)
            self.data_submitAll = {
                "payPwd": 111111,
                "id": submit_cookies,
                "token": submit_token,
            }

            request_response_submitAll = self.client.send(data=json.dumps(self.data_submitAll))
            
            
            
            #解密和验签
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