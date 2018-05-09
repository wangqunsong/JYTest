#coding=utf-8
import re
import json
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
import requests
from base64 import b64encode, b64decode
import rsa

#单次加密串的长度最大为 (key_size/8)-11
'''
加密的 plaintext 最大长度是 证书key位数/8 - 11, 例如1024 bit的证书，被加密的串最长 1024/8 - 11=117,
那么对于 2048bit的证书，被加密的长度最长2048/8 - 11 =245,
解决办法是 分块 加密，然后分块解密就行了，
因为 证书key固定的情况下，加密出来的串长度是固定的。
'''
def rsa_encrypt(msg,pubkey):
    pub_title=pubkey
    pubkey_str="""-----BEGIN PUBLIC KEY-----""" + '\n' + pub_title + '\n' + """-----END PUBLIC KEY-----"""
    msg = msg.encode(encoding="utf-8")
    length = len(msg)
    default_length = 245
    # 公钥加密
    pubobj = Cipher_pkcs1_v1_5.new(RSA.importKey(pubkey_str))
    # 长度不用分段
    if length < default_length:
        encry_text = base64.b64encode(pubobj.encrypt(msg))  # 通过生成的对象加密message明 # 对传递进来的用户名或密码字符串
        encry_value = encry_text.decode('utf8')
        return encry_value
    # 需要分段
    offset = 0
    res = []
    while length - offset > 0:
        if length - offset > default_length:
            res.append(base64.b64encode(pubobj.encrypt(msg[offset:offset + default_length])).decode("utf-8"))
        else:
            res.append(base64.b64encode(pubobj.encrypt(msg[offset:])).decode("utf-8"))
        offset += default_length
    return "".join(res)

if __name__ == '__main__':
    pubkey='MIIBIjANBgkqeriG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxq+EkcWV+gB/B81dqK+WJM1/0qgCS0uFodLv/uygtNTKf4mbHwfy/90SPILkpqkO31F3B5MYyLkl9MQFuA9DD95fcFOQFL7wEUnAtnGbzRbVCqo2JcUpyWV79LDeFlsL87NMvwtIGf5geEDLLPT7WS63X6o3LAaWrro3Z/rzf6zwKSWnzoMhjcrV6inwwkLGpOMQxwOgteaLmYvJ8x3BayokTGRDOH2JMMw49C9c5S2mwJ+axkAdi0ei83Y5K5WcCEbxeNaxZiDZs9HN428/QJtOtcXPtp0PyUH3449ycwBjYF+HHjxihvs/PzI/agPWVtE4hGba1Ldya5JMGh7KKQIDAQAB'
    login_url = 'http://xx.yy.zz.com/api/user/type'
    login_data = {"loginName": "hi@qq.com", "password": "1234test", "loginType": "email", "key": "123445678dfghj"}
    headers_1 = {'Referer': 'http://xx.yy.zz.com', 'Content-Type': 'application/json'}
    r = requests.post(url=login_url, data=json.dumps(login_data), headers=headers_1)
    r.encoding = 'utf-8'
    json_data = json.loads(r.text)
    #print("登录的结果返回值是:\n", json_data)
    token = json_data['data']['token']
    #print("登录的token是:\n", token)
    headers_2 = {'Referer': 'http://xx.yy.zz.com',
                 'Content-Type': 'application/json',
                 'x-Api-token': token}
    msg='{"newPwd": "1234abcd", "origin": "abcd1234", "verified": "1234abcd"}'
    print("未加密前的接口数据是:\n",msg)
    test_data=rsa_encrypt(msg,pubkey)
    print("接口测试传参结果是:\n",test_data)
    test_url_pwd='http://xx.yy.zz.com/api/user/pwd/modify'
    test_r=requests.post(url=test_url_pwd,data=test_data,headers=headers_2)
    test_json_data=json.loads(test_r.text)
    print("接口测试结果是:\n",test_json_data)