# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/2 16:03
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : RSA.py
# @Software: PyCharm
"""
from urllib.parse import quote_plus
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from base64 import b64encode, b64decode


class SHA1withRSA(object):
    '''
    SHA1withRSA签名验签类
    '''

    def __init__(self):
        self.__private_key = 'D:/keys/merchant/rsa_private_key_2048.pem'
        self.__public_key = 'D:/keys/merchant/rsa_public_key_2048.pem'

    def gen_str(self, quoted=0):
        """生成字符串参数集
        :quoted:  bool 是否对字符串编码
        :returns: str  排序后参数集
        """
        self.__parameters = {
            k: quote_plus(v) for k, v in self.__parameters.items()} \
            if quoted else self.__parameters
        return '&'.join(
            '{}={}'.format(k, v) for k, v in sorted(self.__parameters.items()))

    def sign(self, unsigned_str):
        '''
        签名函数
        :param unsigned_str: 待验签字符串
        :return: str 签名字符串
        '''
        with open(self.__private_key, 'r') as f:
            private_key = RSA.importKey(f.read())
        signer = PKCS1_v1_5.new(private_key)
        digest = SHA.new()
        digest.update(unsigned_str.encode())
        sign = signer.sign(digest)
        return b64encode(sign).decode()

    def sync_check_sign(self, msg, signature):
        """同步验签
        :msg:       str 待验签信息
        :signature: str 签名
        :returns:   bool
        """
        with open(self.__public_key) as f:
            rsakey = RSA.importKey(f.read())
        verifier = PKCS1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(msg.encode())
        return verifier.verify(digest, b64decode(signature))
