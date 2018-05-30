# -*- coding: utf-8 -*-

import xlwt
import xlrd
from datetime import date, datetime


class ConfigExcel(object):
    """excel operation class"""

    def __init__(self):
        pass

    def read_excel(self):
        # 打开xlsx文件
        Workbook = xlrd.open_workbook(r'data/case.xlsx')

        # 获取所有sheet
        print(Workbook.sheet_names())  # [u'sheet1', u'sheet2']

        # 根据sheet索引获取sheet内容，以下分别通过sheet索引和名称获取表
        # 故以下sheet1和sheet2获取的是统一个表格"Sheet2"
        sheet1 = Workbook.sheet_by_index(1)
        sheet2 = Workbook.sheet_by_name('Sheet2')

        # 获取sheet的行数和列数
        sheet_name = sheet2.name
        sheet_rows = sheet2.nrows
        sheet_cols = sheet2.ncols
        print(sheet_name, sheet_rows, sheet_cols)

        # 获取整行和整列的值（dict），行数和列数都从0开始计数
        rows = sheet2.row_values(3)  # 获取第四行内容
        cols = sheet2.col_values(0)  # 获取第三列内容
        print(rows)
        print(cols)

        # 获取单元格内容
        print(sheet2.cell(3, 0).value.encode('utf-8'))
        print(sheet2.cell_value(3, 0).encode('utf-8'))

        # 获取单元格数据类型
        # python读取excel中单元格的内容返回的有5种类型，ctype:
        # 0 empty,
        # 1 string,
        # 2 number,
        # 3 date,
        # 4 boolean,
        # 5 error
        print(sheet2.cell(3, 0).ctype)


if __name__ == '__main__':
    excel = ConfigExcel()
    excel.read_excel()
