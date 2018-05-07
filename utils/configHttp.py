# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 15:15
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : configHttp.py
# @Software: PyCharm
"""
"""
添加用于接口测试的client，对于HTTP接口添加HTTPClient，发送http请求。
还可以封装TCPClient，用来进行tcp链接，测试socket接口。
"""

import requests
from utils.log import logger


METHODS = [
    'GET',
    'POST',
    'HEAD',
    'TRACE',
    'PUT',
    'DELETE',
    'OPTIONS',
    'CONNECT']


class UnSupportMethodException(Exception):
    """当传入的method的参数不是支持的类型时抛出此异常。"""
    pass


class HTTPClient(object):
    def __init__(
        self,
        url,
        method='POST',
        headers=None,
        cookies=None,
        params=None,
        timeout=None):
        '''
        初始化HTTPClient类
        :param url: 请求的url地址
        :param method: 请求方法，范围见METHODS列表
        :param headers: 请求头，类型为字典，例：headers={'Content_Type':'text/html'}
        :param cookie: cookie，类型为字典
        :param data: 请求上传的数据(post)
        :param params: 请求上传数据（get）
        :param timeout: 超时时间，格式为int, float or None
        '''
        self.url = url
        self.session = requests.session()
        self.method = method
        self.timeout = timeout
        if self.method not in METHODS:
            raise UnSupportMethodException(
                '不支持的method:{0}，请检查请求方法是否正确！'.format(
                    self.method))
        self.set_headers(headers)
        self.set_params(params)
        self.set_cookies(cookies)

    def set_headers(self, headers):
        if headers:
            self.session.headers.update(headers)

    def set_cookies(self, cookies):
        if cookies:
            self.session.cookies.update(cookies)

    def set_params(self, params):
        if params:
            self.session.params.update(params)

    def send(self, params=None, data=None, **kwargs):
        response = self.session.request(
            method=self.method,
            timeout=self.timeout,
            url=self.url,
            params=params,
            data=data,
            **kwargs)
        response.encoding = 'utf-8'
        logger.debug('{0} {1}'.format(self.method, self.url))
        logger.debug('请求成功: {0}\n{1}'.format(response, response.text))
        return response
