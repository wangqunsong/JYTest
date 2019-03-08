# -*- coding: utf-8 -*-
"""
# @Time    : 2019/3/6 14:53
# @File    : configDB.py
# @Software: PyCharm
# @PythonVersion: 3.5.2
# @desc: 数据库模型类
"""
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class API(Base):
    #表名称
    __tablename__ = "api"
    
    #api表里包含的字段
    id = Column(Integer,primary_key=True,autoincrement=True)
    method = Column(String(length=10),nullable=False)
    name = Column(String(length=50), nullable=False)
    url = Column(String(length=100), nullable=False)
    body = Column(String(length=10), nullable=False)
    project_id = Column(Integer)

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer)
    
    
    
