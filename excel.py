# -*- coding: utf-8 -*-            
# @Author : 测试小牛
# @Time : 12/08/2023 17:35
import openpyxl

def read_excel_value(file_path, row, column):
    # 打开Excel文件
    workbook = openpyxl.load_workbook(file_path)

    # 选择第一个工作表（如果有多个工作表的话）
    worksheet = workbook.active

    # 读取指定行和列的值
    value = worksheet.cell(row=row, column=column).value

    return value

