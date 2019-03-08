#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/6 21:35
# @python  : python3.5
# @File    : CG2003.py
# @Software: PyCharm
# @Des:
import ddt
import unittest
from ddt import file_data

@ddt
class TestCG2003(unittest.TestCase):

    @file_data('./config/cg2003.yaml')
    def setUp(self):
        pass


    def test_cg20003(self,**test_data):
        pass


    def tearDown(self):
        pass
