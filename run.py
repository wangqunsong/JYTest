# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/8 14:42
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : run.py
# @Software: PyCharm
"""
import unittest
import time
from utils import HTMLTestRunner
from utils import configBase
from utils.configBase import Config
from utils.log import MyLog as Log
from utils.configEmail import MyEmail


class Test(object):
    '''
    测试类
    '''

    def __init__(self):
        log = Log.get_log()
        config = Config().get('email')
        self.logger = log.get_logger()
        self.reportPath = log.get_report_path()
        self.onOff = config.get('email_on_off', 2)
        self.caseListFile = configBase.CASE_LIST_FILE
        self.caseFile = configBase.CASE_FILE
        self.caseList = []
        self.email = MyEmail.get_email()

    def set_case_list(self):
        '''
        设置 case list
        :return:
        '''
        with open(self.caseListFile, 'r') as f:
            for value in f.readlines():
                data = str(value)
                if data != '' and not data.startswith("#"):
                    self.caseList.append(data.replace("\n", ""))

    def set_case_suite(self):
        '''
        设置 case suite
        :return:
        '''
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1]
            print(case_name + '.py')
            discover = unittest.defaultTestLoader.discover(
                self.caseFile, pattern=case_name + '*.py', top_level_dir=None)
            suite_module.append(discover)

        if len(suite_module) > 0:
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None
        return test_suite

    def run(self):
        '''
        运行测试case
        :return:
        '''
        try:
            suite = self.set_case_suite()
            now = time.strftime(
                "%Y-%m-%d %H-%M-%S",
                time.localtime(
                    time.time()))
            report = self.reportPath + '\\' + now + '--' + 'JYTest-Report.html'
            #report = self.reportPath + '\\' + 'HTTP-Report.html'
            if suite is not None:
                self.logger.info("********测试开始********")
                with open(report, 'wb') as f:
                    runner = HTMLTestRunner.HTMLTestRunner(
                        f, title='JYTest接口测试', description='小小王的接口测试')
                    runner.run(suite)
            else:
                self.logger.info("未找到测试case，请检查caselist")
        except Exception as ex:
            self.logger.error(str(ex))
        finally:
            self.logger.info("********测试结束********")
            if self.onOff == 'on':
                self.email.send_email()
            elif self.onOff == 'off':
                self.logger.info("邮件发送开关为off,不发送邮件！")
            else:
                print(self.onOff)
                self.logger.info("读取配置文件错误，请联系小小王！")


if __name__ == '__main__':
    test = Test()
    test.run()
