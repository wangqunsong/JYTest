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
from logging.handlers import TimedRotatingFileHandler
from utils.config import LOG_PATH, Config


class Logger(object):
    def __init__(self, logger_name='JYTest'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)

        config = Config().get('log')
        self.log_file_name = config.get(
            'file_name') if config and config.get('file_name') else 'test.log'
        self.backup_count = config.get(
            'backup') if config and config.get('backup') else 5
        # 设置日志输出
        self.console_output_level = config.get(
            'console_level') if config and config.get('console_level') else 'WARNING'
        self.file_output_level = config.get(
            'file_level') if config and config.get('file_level') else 'DEBUG'
        pattern = config.get('pattern') if config and config.get(
            'pattern') else '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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


logger = Logger().get_logger()
