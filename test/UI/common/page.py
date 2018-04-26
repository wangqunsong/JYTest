# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/26 14:47
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : page.py
# @Software: PyCharm
"""

from test.UI.common import Browser

class Page(Browser):
    
    
    def __init__(self, page=None, browser_type='chrome'):
        if page:
            self.driver = page.driver
        else:
            super(Page,self).__init__(browser_type=browser_type)
            
    def get_driver(self):
        return self.driver
    
    def find_element(self, *args):
        return self.driver.find_element(*args)
    
    def find_elements(self, *args):
        return self.driver.find_elements(*args)