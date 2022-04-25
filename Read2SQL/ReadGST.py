# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario 
 @File: ReadGST.py
 @IDE: PyCharm 
 @Author: Sunh98
 @Date: 2022/4/25
        10:23
 @Email: 21120240@bjtu.edu.cn

"""

from SQLFunction import SQL
import NmeaFunc
import os
import win32ui

def SelectandGet():
    dlg = win32ui.CreateFileDialog(1)
    # dlg.SetOFNInitalDir("")
    dlg.DoModal()
    path = dlg.GetPathName()
    return path

if __name__ == '__main__':
    mydb = SQL("ringway")
    date = '210612'
    path_in = SelectandGet()
    with open(path_in, encoding='utf-8') as f_in:
        line = f_in.readline()
        temp = line.strip().split(',')
        while line:
            if 'GST' in temp[0]:
                GST_dict = NmeaFunc.ReadGST(line)
                mydb.writein('GST' + date, GST_dict)
            line = f_in.readline()
            temp = line.strip().split(',')
        print("Finished Write Into Database!\n")
        f_in.close()
