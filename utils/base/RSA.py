# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/2 16:03
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : RSA.py
# @Software: PyCharm
"""
# from urllib.parse import quote_plus
import json
# from Crypto.Hash import SHA
# from Crypto.PublicKey import RSA
# from Crypto.Signature import PKCS1_v1_5
# from base64 import b64encode, b64decode
# import base64
# from Crypto.Hash import SHA
# from Crypto import Random
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
# from Crypto.PublicKey import RSA as rsa
# from Crypto.Cipher import PKCS1_v1_5
from testCase.Interface.test_185_CG1001 import TestCG1001

from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_v1_5


class SHA1withRSA(object):
    '''
    SHA1withRSA签名验签类
    '''

    # def gen_str(self, quoted=0):
    #     """生成字符串参数集
    #     :quoted:  bool 是否对字符串编码
    #     :returns: str  排序后参数集
    #     """
    #     self.__parameters = {
    #         k: quote_plus(v) for k, v in self.__parameters.items()} \
    #         if quoted else self.__parameters
    #     return '&'.join(
    #         '{}={}'.format(k, v) for k, v in sorted(self.__parameters.items()))

    def rsa_long_encrypt(pub_key_str, msg, length=100):
        """
        单次加密串的长度最大为 (key_size/8)-11
        1024bit的证书用100， 2048bit的证书用 200
        """
        pubobj = rsa.importKey(pub_key_str)
        pubobj = PKCS1_v1_5.new(pubobj)
        res = []
        for i in range(0, len(msg), length):
            res.append(pubobj.encrypt(msg[i:i + length]))
        return "".join(res)
    # def sign(self, unsigned_str, pub_key_str):
    #     '''
    #     加密
    #     :param unsigned_str:未加密的字符串
    #     :return: 加密后的密文
    #     '''
    #     with open(pub_key_str, 'r') as f:
    #         key = RSA.importKey(f.read())
    #         h = SHA.new(unsigned_str.encode())
    #         cipher = Cipher_pkcs1_v1_5.new(key)
    #         ciphertext = cipher.encrypt(unsigned_str.encode() + h.digest())
    #         # ciphertext = base64.b64encode(cipher.encrypt(message.encode()))
    #     return ciphertext
    #
    # def sync_check_sign(self, msg, signature):
    #     """同步验签
    #     :msg:       str 待验签信息
    #     :signature: str 签名
    #     :returns:   bool
    #     """
    #     with open(signature) as f:
    #         rsakey = RSA.importKey(f.read())
    #     verifier = PKCS1_v1_5.new(rsakey)
    #     digest = SHA.new()
    #     digest.update(msg.encode())
    #     return verifier.verify(digest, b64decode(signature))

if __name__ == '__main__':
    private_key = 'D:/keys/merchant/rsa_private_key_2048.pem'
    public_key = 'D:/keys/merchant/rsa_public_key_2048.pem'
    jsonData = TestCG1001.cg1001_json
    str = json.dumps(jsonData)
    rsa = SHA1withRSA()
    print(rsa.rsa_long_encrypt(public_key,str))
    
     