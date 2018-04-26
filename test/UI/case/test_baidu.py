# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/25 14:28
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : test_baidu.py
# @Software: PyCharm
"""

import time
import unittest

from test.UI.page.baidu_results_page import BaiDuMainPage, BaiDuResultPage
from utils.config import Config, DATA_PATH
from utils.file_load import ExcelLoad
from utils.log import logger


class TestBaidu(unittest.TestCase):
    target_url = Config().get('target_url')
    baidu_excel = DATA_PATH + '/baidu.xlsx'

    def sub_setUp(self):
        self.page = BaiDuMainPage(
            browser_type='chrome').get(
            self.target_url,
            maximize_window=True)

    def sub_tearDown(self):
        self.page.quit()

    def test_search(self):
        datas = ExcelLoad(self.baidu_excel).data
        for d in datas:
            with self.subTest(data=d):
                self.sub_setUp()
                self.page.search(d['search'])
                time.sleep(2)
                self.page = BaiDuResultPage(self.page)
                links = self.page.result_links
                for link in links:
                    logger.info(link.text)
                self.sub_tearDown()


if __name__ == '__main__':
    unittest.main(verbosity=2)
