# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 9:08
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : run_test_baidu.py
# @Software: PyCharm
"""

import time
import unittest

from testCase.UI.case import TestBaidu
from utils.HTMLTestRunner import HTMLTestRunner
from utils.configBase import REPORT_PATH

if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(time.time()))
    #report_path = REPORT_PATH + '\\' + now + '--' + 'HMLReport.html'
    report = REPORT_PATH + '\\' + 'HMLReport.html'
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBaidu))

    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, title='金运通测试报告', description='小小王测试')
        runner.run(suite)
    
    # e = Email(title='百度搜索测试报告',
    #           message='这是今天的测试报告，请查收！',
    #           receiver='',
    #           server='',
    #           sender='',
    #           password='',
    #           path=report_path
    #           )
    # e.send()