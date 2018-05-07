# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 14:59
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : baidu_results_page.py
# @Software: PyCharm
"""

from selenium.webdriver.common.by import By

from testCase.UI.page.baidu_main_page import BaiDuMainPage


class BaiDuResultPage(BaiDuMainPage):
    loc_result_links = (By.XPATH, '//div[contains(@class, "result")]/h3/a')
    
    
    @property
    def result_links(self):
        return self.find_elements(*self.loc_result_links)