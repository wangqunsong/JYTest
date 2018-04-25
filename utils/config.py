# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/25 14:43
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : config.py
# @Software: PyCharm
"""

import os
from utils.file_load import YamlLoad

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')


class Config(object):
    def __init__(self, config=CONFIG_FILE):
        self.config = YamlLoad(config).data

    def get(self, element, index=0):
        """
        用YamlLoad读取返回的是一个list，第一项是默认的节，如果有多个节，可以传入index来获取。
        """
        return self.config[index].get(element)
