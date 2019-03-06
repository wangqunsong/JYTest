# -*- coding: utf-8 -*-
"""
# @Time    : 2018/10/8 9:59
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : configYML.py
# @Software: PyCharm
"""
import os
import codecs
import yaml
from utils.configBase import BASE_PATH

class ConfigYML:
    def __init__(self,case_file):
        self.case_file = case_file
    
    def load_case(self):
        with open(self.case_file,'rb') as f:
            yml_case_file = list(yaml.safe_load_all(f))
        order = []
        a = list(yml_case_file[0].keys())
        for i in range(0, len(a)):
            c = []
            # print(yml_cg2002[0].get(a[i]))
            len_case = len(yml_case_file[0].get(a[i]))
            for j in range(0, len_case):
                c.append(''.join(list(yml_case_file[0].get(a[i])[j].values())))
                if (len(c) == len_case):
                    order.append(c)
        return order
    
if __name__ == '__main__':
    case_file = os.path.join(BASE_PATH, 'testCase/CaseList/CG2002.yml')  # .yml用例文件路径
    yml_case = ConfigYML(case_file).load_case()
    print(yml_case)