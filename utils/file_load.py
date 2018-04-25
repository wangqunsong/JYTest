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
