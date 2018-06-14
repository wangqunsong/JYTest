
import xlrd
import os
from utils.configBase import DATA_PATH


class TestCG2001():
    '''
    TestCG2001测试类
    '''
    
    def setParameters(self, *args):
        xlsPath = os.path.join(DATA_PATH, 'case.xlsx')
        Workbook = xlrd.open_workbook(xlsPath)
        sheet = Workbook.sheet_by_name('CG2001')
        params = sheet.row_values(0)
        me = []
        for i in range(len(params)):
            me.append(str(params[i]))
        print(me)
            
        
if __name__ == '__main__':
    cg2001 = TestCG2001()
    cg2001.setParameters()