# -*- coding: utf-8 -*-
"""
# @Time    : 2018/7/27 11:31
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : configSQL.py
# @Software: PyCharm
"""

import pymysql
db = pymysql.connect(host='10.10.10.50',port=3308,user='eqqtst',password='eqqtst',database='eqqtst')

cursor = db.cursor()

cursor.execute("SELECT BIZ_FLOW,VERIFY_CODE FROM t_biz_sms_message WHERE phone_no = '18392169938' ORDER BY  create_time DESC LIMIT 1")

message = cursor.fetchall()
print(message)

cursor.close()
db.close()