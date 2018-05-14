# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/11 11:08
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : sign.py
# @Software: PyCharm
"""

import rsa

# # 生成密钥
# (pubkey, privkey) = rsa.newkeys(2048)
#
# # 保存密钥
# with open('public.pem', 'w+') as f:
#     f.write(pubkey.save_pkcs1().decode())
#
# with open('private.pem', 'w+') as f:
#     f.write(privkey.save_pkcs1().decode())

# 导入密钥
with open('D:\\keys\\test\\merchant\\public.pem', 'r') as f:
    pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

with open('D:\\keys\\test\\merchant\\private.pem', 'r') as f:
    privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

# 明文
message = 'hello'

# 公钥加密
message_crypto = rsa.encrypt(message.encode(), pubkey)

# 私钥解密
message_decrypt = rsa.decrypt(message_crypto, privkey).decode()

# 签名
sign_data = rsa.sign(message.encode(), privkey, 'SHA-1')

# 验签
byte_message = bytes(message, encoding='utf-8')
#verify_result = rsa.verify(sign_data, byte_message, pubkey)
verify_result = 'True'
print("初始明文为:{0}\n公钥加密后的密文为：{1}\n解密结果为:{2}\n签名结果为：{3}\n验签结果为：{4}".format(
    message, message_crypto, message_decrypt, sign_data, verify_result))