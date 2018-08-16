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
from utils.configHttp import HTTPClient
from utils.configHttpHeader import Header
from utils.log import logger
import http.cookiejar as cookielib


@paramunittest.parametrized(*cg1044)
class TestCG1044(unittest.TestCase):
    '''
    TestCG1044测试类
    '''

    def setParameters(
            self,
            caseName,
            registerPhone,
            merchantNo,
            custType,
            callbackUrl,
            responsePath,
            cardNo,
            code,
            name,
            phone,
            mailAddr,
            idNo,
            tradeCode,
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
        self.idNo = str(idNo)
        self.respCode = str(respCode)

    def setUp(self):
        self.interface_url = Config().get('cg1044')
        self.sign_encrypt_url = "http://192.168.20.128:8081/sign_and_encrypt"
        self.decrypt_and_verify_url = "http://192.168.20.128:8081/decrypt_and_verify"

        self.submit_url = "http://10.10.10.185:9008/dep-page-service/submit"
        self.submit_all_url = "http://10.10.10.185:9008/dep-page-service/submitAll"
        self.common_send_message_url = "http://10.10.10.185:9008/dep-page-service/sendSms?"

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
                "responsePath": self.responsePath
            }
        }

        # 签名和加密
        # 加密
        self.request_string = json.dumps(cg1044_json)
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

    def test_cg1044(self):
        # 请求返回的密文
        try:
            request_response_cg1044 = self.client.send(data=self.data)
            token = request_response_cg1044.cookies.get_dict()['token']
            id = request_response_cg1044.cookies.get_dict()['id']
            message = request_response_cg1044.cookies.get_dict()['message']
            #JSESSIONID = request_response_cg1044.cookies.get_dict()['JSESSIONID']

            cookies = dict(message=message, id=id, token=token)

            # 获取验证码
            requests_message_url = self.common_send_message_url + "phoneNo=" + \
                self.phone + "&token=" + token + "&merOrderNo=" + self.merOrderNo
            print(requests_message_url)
            self.client_message = HTTPClient(
                url=requests_message_url,
                method='GET',
                timeout=10,
                headers=self.http_header,
                cookies=cookies)

            self.data_message = {
                "phoneNo": self.phone,
                "token": token,
                "merOrderNo": self.merOrderNo
            }

            request_validateParam_url = "http://10.10.10.185:9008/dep-page-service/validateParam"
            self.client_validateParam = HTTPClient(
                url=request_validateParam_url,
                method='POST',
                timeout=10,
                headers=self.http_header,
                cookies=cookies
            )
            self.data_validateParam = {
                "idNo": self.idNo,
                "merchantNo": self.merchantNo,
                "merOrderNo": self.merOrderNo
            }
            request_response_validateParam = self.client_validateParam.send(
                data=self.data_validateParam)
            request_response_message = self.client_message.send(
                data=self.data_message)

            # submit
            self.client_submit = HTTPClient(
                url=self.submit_url,
                method='POST',
                timeout=10,
                headers=self.http_header,
                cookies=cookies
            )
            self.data_submit = {
                "cardNo": self.cardNo,
                "code": 485125,
                "idNo": self.idNo,
                "name": self.name,
                "phone": self.phone,
                "smsCode": 485125,
                "mobile": self.registerPhone,
                "merchantNo": self.merchantNo,
                "merOrderNo": self.merOrderNo,
                "id": id,  # 需要修改id的值
                "token": token,
                "mailAddr": self.mailAddr
            }

            # request_response_submit = requests.post(self.submit_url,data=self.data_submit,headers=self.http_header)
            request_response_submit = self.client_submit.send(
                data=self.data_submit)
            submit_token = token
            submit_cookies = token

            # submitAll
            self.client_submitAll = HTTPClient(
                url=self.submit_all_url,
                method='POST',
                timeout=10,
                headers=self.http_header,
                cookies=cookies
            )
            self.data_submitAll = {
                "payPwd": 111111,
                "id": submit_cookies,
                "token": submit_token,
            }

            # request_response_submitAll = requests.post(self.submit_all_url,data=self.data_submitAll,headers=self.http_header)
            request_response_submitAll = self.client_submitAll.send(
                data=self.data_submitAll)
            respCode = request_response_submitAll.status_code
            self.assertEquals(respCode, 200)
            # logger.error(self.request_response_submitAll.text)
            print("恭喜，开户成功！")
        except requests.exceptions.ConnectTimeout:
            raise TimeoutError

    def tearDown(self):
        try:
            pass
        except requests.exceptions.ConnectTimeout:
            raise TimeoutError


if __name__ == '__main__':
    unittest.main()
