# -*- coding: utf-8 -*-
"""
# @Time    : 2018/5/15 10:00
# @Author  : wangqunsong
# @Email   : wangqunsong@hotmail.com
# @File    : configJPype.py
# @Software: PyCharm
"""

import os
import jpype
from jpype import *


class ConfigJVM(object):
    def __init__(self):
        self.BASE_PATH = os.path.split(
            os.path.dirname(
                os.path.abspath(__file__)))[0]
        self.jarpath = os.path.join(self.BASE_PATH, 'jar/support.jar')
        self.depend_jar_path = os.path.join(self.BASE_PATH, 'jar/depend')

    def start_jvm(self):
        jpype.startJVM(
            getDefaultJVMPath(),
            "-Djava.class.path=" +
            self.jarpath,
            "-Djava.ext.dirs=" +
            self.depend_jar_path)  # 当有依赖的JAR包存在时，一定要使用-Djava.ext.dirs参数进行引入
        if not isJVMStarted():
            jpype.startJVM(
                getDefaultJVMPath(),
                "-Djava.class.path=" +
                self.jarpath,
                "-Djava.ext.dirs=" +
                self.depend_jar_path)

    def shutdown_jvm(self):
        jpype.shutdownJVM()


if __name__ == '__main__':
    jvm_test = ConfigJVM()
    jvm_test.start_jvm()
    test_rsa = JClass('jyt.TestRSACert')
    main_test = test_rsa.main([])
    jvm_test.shutdown_jvm()
