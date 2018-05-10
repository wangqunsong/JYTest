# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/2 15:06
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : DES.py
# @Software: PyCharm
"""
import binascii
from pyDes import des, CBC, PAD_PKCS5
from utils.base.generator import random_str


class DesEncrypt(object):

    def __init__(self):
        self.key = self.key_generrate()

    def key_generrate(self):
        return random_str(8, 8)

    def des_encrypt(self, s):
        """
        DES 加密
        :param s: 原始字符串
        :return: 加密后字符串，16进制
        """
        secret_key = self.key
        iv = secret_key
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        en = k.encrypt(s, padmode=PAD_PKCS5)
        return str(binascii.b2a_hex(en), encoding="utf-8")

    def des_to_hex(self, encrypted_string):
        '''
        sign转hex函数
        :param signed_string: 加密后的信息
        :return: 转换后的hex字符串
        '''
        return str(
            binascii.hexlify(
                bytes(
                    encrypted_string,
                    encoding="utf8")),
            encoding="utf8")

    def des_descrypt(self, s):
        """
        DES 解密
        :param s: 加密后的字符串，16进制
        :return:  解密后的字符串
        """
        secret_key = self.key
        iv = secret_key
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
        return str(de, encoding="utf-8")


if __name__ == '__main__':
    encrypt = DesEncrypt()
    test_string = "1234567890"
    encrypted_string = encrypt.des_encrypt(test_string)
    jsonEnc = encrypt.des_to_hex(encrypted_string)
    descrypt_string = encrypt.des_descrypt(encrypted_string)
    print("原始信息为:{0}\n加密后的信息为：{1}\n转换为hex字符串为：{2}\n解密结果为：{3}".format(
        test_string, encrypted_string, jsonEnc, descrypt_string))
