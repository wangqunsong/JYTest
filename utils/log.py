# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/25 15:10
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : log.py
# @Software: PyCharm
"""


import os
import logging
import threading
from logging.handlers import TimedRotatingFileHandler

from utils import configBase
from utils.configBase import LOG_PATH, Config



class Log(object):
    def __init__(self, logger_name='JYTest'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.INFO)

        config = Config().get('log')
        self.log_file_name = config.get(
            'file_name', 2) if config and config.get('file_name') else 'test.log'
        self.backup_count = config.get(
            'backup', 2) if config and config.get('backup') else 5
        # 设置日志输出
        self.console_output_level = config.get(
            'console_level', 2) if config and config.get('console_level') else 'WARNING'
        self.file_output_level = config.get(
            'file_level', 2) if config and config.get('file_level') else 'DEBUG'
        pattern = config.get('pattern') if config and config.get(
            'pattern', 2) else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.formatter = logging.Formatter(pattern)
        

    def get_logger(self):
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 日志文件保留backup_count份
            file_handler = TimedRotatingFileHandler(
                filename=os.path.join(
                    LOG_PATH,
                    self.log_file_name),
                when='D',
                interval=1,
                backupCount=self.backup_count,
                delay=True,
                encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger
    
    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " 请求开始--------")

    def build_end_line(self, case_no):
        """
        write end line
        :return:
        """
        self.logger.info("--------" + case_no + " 请求结束--------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name+" - Code:"+code+" - msg:"+msg)

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = configBase.REPORT_PATH
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return LOG_PATH

    def write_result(self, result):
        """

        :param result:
        :return:
        """
        result_path = os.path.join(LOG_PATH, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            logger.error(str(ex))
            
class MyLog(object):
    log = None
    mutex = threading.Lock()
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()
        
        return MyLog.log


logger = Log().get_logger()

if __name__ == "__main__":
    log = MyLog.get_log()
    logger = log.get_logger()
    logger.debug("test debug")
    logger.info("test info")


