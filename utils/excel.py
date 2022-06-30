import os
import xlrd
from xlutils.copy import copy
from utils.logger import log
from config.conf import cm

'''
读取/写入数据（Excel）
'''

class OperateExcel:

    def __init__(self, table_name, sheet_name):
        """确认Excel和sheet存在"""
        dir_path = cm.BASE_DIR
        self.name = sheet_name
        self.path = os.path.join(dir_path, r'projects\web_uitest\TestData', table_name)  # 路径配置
        try:
            self.rwexcel = xlrd.open_workbook(self.path, encoding_override='utf-8')
            self.shelldata = self.rwexcel.sheet_by_name(self.name)
        except Exception as e:
            log.error("没有用例Excel，请创建并确认有数据", e)

    def get_all_data(self):
        """获取表中某个shell所有的数据"""
        try:
            data = []
            countrows = self.shelldata.nrows  # 总行数
            for i in range(countrows):
                rowdata = self.shelldata.row_values(i)
                if rowdata[0] != 'case_name':
                    data.append(rowdata)
            return data
        except BaseException:
            log.error("Excel文件错误")
            raise xlrd.XLRDError('xlrd异常中断')

    def get_row_data(self, rowIndex):
        """获取某一行的数据"""
        return self.shelldata.row_values(rowIndex)

    def get_col_data(self, colIndex):
        """获取某一列的内容"""
        return self.shelldata.col_values(colIndex)

    def get_cell_value(self, row, col):
        """获取某一个单元格的内容"""
        return self.shelldata.cell_value(row, col)

    def get_col_name_num(self, col_name):
        """根据列名获取列号"""
        data_one_row = self.get_row_data(0)  # 获取第一行字段数据
        check = False
        col_index = 0
        for data in data_one_row:  # 遍历寻找符合名字的列的列数
            if data == col_name:
                check = True
                break
            else:
                col_index += 1
        if check:
            return col_index
        else:
            log.error("列名-{0}不存在".format(col_name))
            raise xlrd.XLRDError('xlrd异常中断')

    def get_col_name_data(self, name):
        """获取特定列名的列数据"""
        col_index = self.get_col_name_num(name)
        try:
            return self.get_col_data(col_index)
        except IndexError:
            log.error('未找到对应列名')

    def write_value(self, row, col, value):  # 该方法仅支持xls格式
        """写入数据"""
        rwexcel = xlrd.open_workbook(self.path, encoding_override='utf-8')
        wb = copy(rwexcel)
        ws = wb.get_sheet(self.name)  # 获取第sheet
        if len(str(value)) > 32767:
            value = str(value)[:32767]
        ws.write(row, col, str(value))  # 修改特定单元格信息
        wb.save(self.path)

    def get_shell_nrow(self):
        """获取shell表总行数"""
        return self.shelldata.nrows

    def get_sheet_index(self, name):
        """根据sheet名称获取其索引值"""
        sheet_names = self.rwexcel.sheet_names()
        check = False
        sheet_index = 0
        for sheet in sheet_names:  # 遍历寻找符合名字的列的列数
            if sheet == name:
                check = True
                break
            else:
                sheet_index += 1
        if check:
            return sheet_index
        else:
            log.error("列名-{0}不存在".format(name))
            raise xlrd.XLRDError('xlrd异常中断')


if __name__ == '__main__':
    excel = OperateExcel("register.xls", "机构注册")
    print(excel.get_row_data(1))
