# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/25 10:29
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : configExcel.py
# @Software: PyCharm
"""
from xlrd import open_workbook
import os

from utils.configBase import DATA_PATH


class ConfigExcel(object):
    
    def __init__(self):
        self.case_path = DATA_PATH
        
    def get_xls_row(self, xls_name, sheet_name):
        """
        get interface data from xls file
        :return:
        """
        cls = []
        # get xls file's path
        xlsPath = os.path.join(self.case_path, xls_name)
        # open xls file
        file = open_workbook(xlsPath)
        # get sheet by name
        sheet = file.sheet_by_name(sheet_name)
        # get one sheet's rows
        nrows = sheet.nrows
        for i in range(nrows):
            if sheet.row_values(i)[0] != u'CaseName':
                cls.append(sheet.row_values(i))
        return cls
    
    def get_xls_cols(self, xls_name, sheet_name):
        """
        get interface data from xls file
        :return:
        """
        cls = []
        # get xls file's path
        xlsPath = os.path.join(self.case_path, xls_name)
        # open xls file
        file = open_workbook(xlsPath)
        # get sheet by name
        sheet = file.sheet_by_name(sheet_name)
        # get one sheet's ncols
        ncols = sheet.ncols
        for i in range(ncols):
            cls.append(sheet.col_values(i)[0])
        return cls
    
if __name__ == '__main__':
    excel_test = ConfigExcel()
    h = excel_test.get_xls_row("case.xlsx", "CG2001")
    h2 = excel_test.get_xls_cols("case.xlsx", "CG2001")
    print(h)
    print(h2)