# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario 
 @File: Span_Nmea_extraction.py
 @IDE: PyCharm 
 @Author: Sunh98
 @Date: 2022/6/28
        12:39
 @Email: 21120240@bjtu.edu.cn

"""

import win32ui
from tqdm import tqdm

def SelectandGet():
    dlg = win32ui.CreateFileDialog(1)
    dlg.DoModal()
    path = dlg.GetPathName()
    return path

def SelectandSave():
    dlg = win32ui.CreateFileDialog(0)
    # dlg.SetOFNInitalDir("")
    dlg.DoModal()
    path = dlg.GetPathName()
    return path

if __name__ == '__main__':
    input_path = SelectandGet()
    output_path = SelectandSave()

    with open(input_path,encoding='utf-8') as f_in:
        count = len(f_in.readlines())
        print("The number of lines of text to be processed is %d" % count)
        f_in.seek(0)  # 计算待处理的数据总量

        with open(output_path, 'a+') as f_out:
            with tqdm(range(count), desc='Text Processing: ') as tbar:
                line = f_in.readline()
                temp = line.strip().split(',')  # 扒皮
                while line:
                    if '$' in temp[0]:
                        f_out.write(line)
                    line = f_in.readline()
                    temp = line.strip().split(',')  # 扒皮
                    tbar.update()
            f_out.close()
