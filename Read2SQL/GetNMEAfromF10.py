# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 12:39:26 2022

@author: sun
"""

import pandas as pd
from pandas import DataFrame
import win32ui
from tqdm import tqdm, trange

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
    with open(path_in, encoding='ISO-8859-15') as f_in:
        with open(path_out, 'a+', encoding='utf-8') as f_out:
            count = len(f_in.readlines())
            print("The number of lines of text to be processed is %d" %count)
            f_in.seek(0)
            line = f_in.readline()
            temp = line.strip().split(',')
            with tqdm(range(count), desc='Text Processing: ') as tbar:
                while line:
                    line = line[line.rfind('$'):]
                    temp = line.strip().split(',')
                    if '$' in temp[0] and (10 >= len(temp[-1]) >= 2) and len(temp)>=5:
                        if temp[-1][-3] == '*':
                            line = line[line.rfind('$'):]
                            f_out.write(line)
                    tbar.update()
                    line = f_in.readline()
                    temp = line.strip().split(',')
                f_out.close()

                
            
        














