# -*- coding: utf-8 -*-
"""
# @Time    : 2018/4/25 14:44
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : file_load.py
# @Software: PyCharm
"""

import yaml
import os
from xlrd import open_workbook


class YamlLoad(object):
    def __init__(self, yaml_file):
        if os.path.exists(yaml_file):
            self.yaml_file = yaml_file
        else:
            raise FileNotFoundError('未找到配置文件')
        self._data = None

    @property
    def data(self):
        if not self._data:
            with open(self.yaml_file, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))

        return self._data


class SheetTypeError(Exception):
    pass


class ExcelLoad(object):
    """
   ExcelLoad类读取excel文件中的内容。返回list。

    如：
    excel中内容为：
    | A  | B  | C  |
    | A1 | B1 | C1 |
    | A2 | B2 | C2 |

    如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
    [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

    如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
    [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

    可以指定sheet，通过index或者name：
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='BaiDuTest')
    """

    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError('excel文件不存在！')
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError(
                    'Please pass in <type int> or <type str>, not {0}'.format(
                        type(
                            self.sheet)))
            elif isinstance(self.sheet, int):
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)  # 首行为title
                for col in range(1, s.nrows):
                    # 依次遍历其余行，与首行组成dict，拼到self._data中
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):
                    # 遍历所有行，拼到self._data中
                    self._data.append(s.row_values(col))
        return self._data


if __name__ == '__main__':
    test_yml_file = 'E:\Git\JYTest\config\config.yml'
    yml_reader = YamlLoad(test_yml_file)
    print(yml_reader.data)

    test_excel_file = 'E:\Git\JYTest\data\\baidu.xlsx'
    excel_reader = ExcelLoad(test_excel_file, title_line=True)
    print(excel_reader.data)
