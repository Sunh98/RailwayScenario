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
from tqdm import tqdm, trange
import NmeaFunc as nf

def SelectandGet():
    dlg = win32ui.CreateFileDialog(1)
    # dlg.SetOFNInitalDir("")
    dlg.DoModal()
    path = dlg.GetPathName()
    return path

if __name__ == '__main__':
    mydb = SQL("ringway")
    date = '191219'
    path_in = SelectandGet()
    mydb.create_table('GST'+date,nf.GSTDict())
    with open(path_in, encoding='utf-8') as f_in:
        count = len(f_in.readlines())
        f_in.seek(0)
        line = f_in.readline()
        temp = line.strip().split(',')
        with tqdm(range(count), desc = 'Processing: ') as tbar:
            while line:
                if 'GST' in temp[0]:
                    GST_dict = NmeaFunc.ReadGST(line)
                    mydb.writein('GST' + date, GST_dict)
                tbar.update()
                line = f_in.readline()
                temp = line.strip().split(',')

            print("Finished Write Into Database!\n")
        f_in.close()
