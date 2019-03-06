# -*- coding: utf-8 -*-
"""
# @Time    : 2019/3/6 15:09
# @File    : test_db.py
# @Software: PyCharm
# @PythonVersion: 3.5.2
# @desc:
"""
from sqlalchemy import create_engine
from utils.configDB import API
from  sqlalchemy.orm import sessionmaker

#连接数据库
engine = create_engine("mysql+pymysql://root:123456@localhost/mockserver?charset=utf8")

#创建会话
session = sessionmaker(engine)
mySession = session()

#查询
result = mySession.query(API).all()
print(result[0])
result1 = mySession.query(API).first()
print(result1.id)
result3 = mySession.query(API).filter_by(id=3).first()
print(result3.url)

#新增
# api = API(method='POST',name='Add',url='127.0.0.1/add',body='body',project_id='ADD')
# mySession.add(api)
# mySession.commit()

#修改
mySession.query(API).filter(API.id==3).update({"method":"POST"})
mySession.commit()