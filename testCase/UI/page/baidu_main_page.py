# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 14:53
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : baidu_main_page.py
# @Software: PyCharm
"""

from selenium.webdriver.common.by import By

from testCase.UI import Page


class BaiDuMainPage(Page):
    loc_search_input = (By.ID, 'kw')
    loc_search_button = (By.ID, 'su')

    def search(self, kw):
        '''搜索'''
        self.\
            find_element(*self.loc_search_input)\
            .send_keys(kw)
        self\
            .find_element(*self.loc_search_button)\
            .click()
