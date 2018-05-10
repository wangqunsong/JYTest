# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/10 16:55
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : RSA.py
# @Software: PyCharm
"""
import base64
import binascii
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from utils.configBase import Config


class Sign(object):
    '''
    签名类
    '''

    def __init__(self):
        '''
        初始化Sign类，读取public_key和private_key
        '''
        config = Config().get('sign')
        self.public_key = config.get('public_key', 2)
        self.private_key = config.get('private_key', 2)

    def sign_string(self, unsigned_string):
        '''
        签名函数
        :param unsigned_string: 待签名的字符串
        :return: 签名后的字符串
        '''
        key = RSA.importKey(open(self.private_key).read())
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA.new(unsigned_string.encode("utf8")))
        # base64 编码，转换为unicode表示并移除回车
        sign = base64.encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def sign_to_hex(self, signed_string):
        '''
        sign转hex函数
        :param signed_string: 签名后的信息
        :return: 转换后的hex字符串
        '''
        return str(
            binascii.hexlify(
                bytes(
                    signed_string,
                    encoding="utf8")),
            encoding="utf8")

    def validate_sign(self, message, signature):
        '''
        验签函数，message为原始信息，signature为使用sign_string函数签名后的信息
        :param message: 原始信息
        :param signature: 签名后的信息
        :return: 验签成功返回True，否则返回False
        '''
        key = RSA.importKey(open(self.public_key).read())
        signer = PKCS1_v1_5.new(key)
        digest = SHA.new()
        digest.update(message.encode("utf8"))
        if signer.verify(
            digest, base64.decodestring(
                signature.encode("utf8"))):
            return True
        return False


if __name__ == '__main__':
    sign = Sign()
    test_string = "1234567890"
    sign_string = sign.sign_string(test_string)
    keyEnc = sign.sign_to_hex(sign_string)
    result = sign.validate_sign(test_string, sign_string)
    print("原始信息为:{0}\n签名后的信息为：{1}\n转换为hex字符串为：{2}\n验签结果为：{3}".format(
        test_string, keyEnc, keyEnc, result))
