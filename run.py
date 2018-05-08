# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/8 14:42
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : run.py
# @Software: PyCharm
"""

import os
import unittest
from utils.log import MyLog as Log
import utils.configBase as Config
from utils.configEmail import Email

localReadConfig = Config.Config()

class Test(object):
    '''
    测试类
    '''
    def __init__(self):
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        onOff = localReadConfig.get('email_on_off')
        self.caseListFile = Config.CASE_LIST_FILE
        self.caseFile = Config.CASE_FILE
        self.caseList = []
        self.email = Email.