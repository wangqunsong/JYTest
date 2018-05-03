# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 15:15
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : client.py
# @Software: PyCharm
"""
"""
添加用于接口测试的client，对于HTTP接口添加HTTPClient，发送http请求。
还可以封装TCPClient，用来进行tcp链接，测试socket接口等等。
"""

import requests
from utils.log import logger


class HTTPClient(object):
    def __init__(self):
        self.url = None
        self.merchantNo = None
        self.jsonEnc = None
        self.keyEnc = None
        self.sign = None
        self.merOrderNo = None
        self.headers = None

    def set_url(self, url):
        if url:
            self.url = url

    def set_headers(self, header):
        if header:
            self.headers = header

    def set_merchant_no(self, merchantNo):
        if merchantNo:
            self.merchantNo = merchantNo

    def set_merOrder_no(self, merOrderNo):
        if merOrderNo:
            self.merchantNo = merOrderNo

    def set_jsonEnc(self, jsonEnc):
        if jsonEnc:
            self.jsonEnc = jsonEnc

    def set_keyEnc(self, keyEnc):
        if keyEnc:
            self.keyEnc = keyEnc

    # http get method

    def get(self):
        try:
            response = requests.get(
                self.url,
                merOrderNo=self.merOrderNo,
                headers=self.headers,
            )
            # response.raise_for_status()
            response.encoding = 'utf-8'
            logger.debug('{0} {1}'.format('GET', self.url))
            logger.debug('请求成功: {0}\n{1}'.format(response, response.text))
            return response
        except TimeoutError:
            logger.debug('请求超时')
            return None

    # http post method
    def post(self):
        try:
            response = requests.post(
                url=self.url,
                headers=self.headers,
                merchantNo=self.merchantNo,
                merOrderNo=self.merOrderNo,
                jsonEnc=self.jsonEnc,
                keyEnc=self.keyEnc,
                sign=self.sign
            )
            # response.raise_for_status()
            response.encoding = 'utf-8'
            logger.debug('{0} {1}'.format('POST', self.url))
            logger.debug('请求成功: {0}\n{1}'.format(response, response.text))
            return response
        except TimeoutError:
            logger.debug('请求超时')
            return None
