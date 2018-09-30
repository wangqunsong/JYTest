# -*- coding: utf-8 -*-
"""
# @Time    : 2018/9/30 10:42
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : wang.py
# @Software: PyCharm
"""

import os
import yaml

from testCase.caseParams.CG1044_params import cg1044
from utils.configBase import Config, BASE_PATH, YamlLoad
from utils.configExcel import ConfigExcel

excel_cg2002 = ConfigExcel().get_xls_row("caselist.xlsx", "CG2002")

CG2002_file = os.path.join(BASE_PATH, 'testCase/CaseList/CG2002.yml')  # .yml配置文件路径
with open(CG2002_file, 'rb') as f:
    yml_cg2002 = list(yaml.safe_load_all(f))

data_test = YamlLoad(CG2002_file).data
print("标准：")
print(excel_cg2002)

print("实际：")
c = []
a = list(yml_cg2002[0].keys())
print("共有 %d 个Case" % len(a))
print(a)
print(yml_cg2002[0])
for i in  range(0,len(a)):
    print(yml_cg2002[0].get(a[i]))
    len_case = len(yml_cg2002[0].get(a[i]))
    for j in range(0,len_case):
        c.extend(''.join(list(yml_cg2002[0].get(a[i])[j].values())))
        print(''.join(list(yml_cg2002[0].get(a[i])[j].values())))
#print(c)
    
