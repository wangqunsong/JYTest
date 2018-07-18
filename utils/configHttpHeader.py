# -*- coding: utf-8 -*-
"""
# @Time    : 2018/7/18 11:42
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : configHttpHeader.py
# @Software: PyCharm
"""

class Header(object):
    '''
    请求报文头类
    '''
    request_headers = {
        "accept-encoding": "gzip, deflate",
        "connection": "Keep-Alive",
        "content-type": "application/json",
        "host": "10.10.10.185:10003"
    }
    encrypt_decrypt_headers = {
            "host": "127.0.0.1",
            "Content-Type": "application/json",
            "connection": "Keep-Alive",
            "accept-encoding": "gzip, deflate"
        }


if __name__ == '__main__':
    h1 = Header().request_headers
    h2 = Header().encrypt_decrypt_headers
    print(h1)
    print(h2)