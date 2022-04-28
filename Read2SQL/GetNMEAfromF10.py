# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 12:39:26 2022

@author: sun
"""

import pandas as pd
from pandas import DataFrame
import win32ui

def SelectandGet():
    dlg = win32ui.CreateFileDialog(1)
    # dlg.SetOFNInitalDir("")
    dlg.DoModal()
    path = dlg.GetPathName()
    return path

def SelectandSave():
    dlg = win32ui.CreateFileDialog(0)
    # dlg.SetOFNInitalDir("")
    dlg.DoModal()
    path = dlg.GetPathName()
    return path

path_in = SelectandGet()
path_out = SelectandSave()

if __name__ == '__main__':
    with open(path_in, encoding='utf-8') as f_in:
        with open(path_out, 'a+', encoding='utf-8') as f_out:
            # count = len(f_in.readlines())
            f_in.seek(0)
            line = f_in.readline()
            temp = line.strip().split(',')
            while line:
                if '$G' in temp[0]:
                    line = line[line.rfind('$'):]
                    f_out.write(line)
                line = f_in.readline()
                temp = line.strip().split(',')
            f_out.close()

                
            
        














