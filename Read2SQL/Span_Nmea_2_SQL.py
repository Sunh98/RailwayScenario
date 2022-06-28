# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario 
 @File: Span_Nmea_2_SQL.py
 @IDE: PyCharm 
 @Author: Sunh98
 @Date: 2022/6/28
        13:14
 @Email: 21120240@bjtu.edu.cn

"""

import win32ui
from SQLFunction import SQL
import NmeaFunc
from tqdm import tqdm

def SelectandGet():
    dlg = win32ui.CreateFileDialog(1)
    dlg.DoModal()
    path = dlg.GetPathName()
    return path

def flagCollection(flags):
    flag_list = []
    for flag in flags:
        flag = flag[-3:]
        if flag not in flag_list:
            flag_list.append(flag)
    return flag_list

def dataBlock2Sql(buffer):
    basic_dict = {}
    for item in buffer:
        temp = item.strip().split(',')
        flag = temp[0][-3:]
        if flag == 'GGA':
            current_time = NmeaFunc.ReadGGA(item)['Time']
            basic_dict = dict(basic_dict, **NmeaFunc.ReadGGA(item))
        elif flag == 'RMC':
            basic_dict = dict(basic_dict, **NmeaFunc.ReadRMC(item))
    end = 0
    return (basic_dict)

if __name__ == '__main__':
    mydb = SQL("ringway")
    date = '220117SPAN'
    input_path = SelectandGet()

    mydb.create_table('BASIC'+date, NmeaFunc.BasicCol())
    #  计算需要处理的数据总量
    with open(input_path, encoding='utf-8') as f_in:
        #  计算需要处理的数据总量
        count = len(f_in.readlines())
        print("The number of lines of text to be processed is %d" % count)
        f_in.seek(0)   #文件指针位置归零
        #  查询数据块标志位
        flags = []
        for i in range(30):
            line = f_in.readline()
            temp = line.strip().split(',')  # 扒皮
            if not line:
                break
            else:
                flags.append(temp[0])
        flag_list = flagCollection(flags)
        f_in.seek(0)  # 文件指针位置归零

        with tqdm(range(count), desc='Text Processing: ') as tbar:
            flag_list_process = []
            buffer = []
            line = f_in.readline()
            temp = line.strip().split(',')  # 扒皮
            while line:
                if temp[0][-3:] not in flag_list_process:
                    flag_list_process.append(temp[0][-3:])
                buffer.append(line)
                line = f_in.readline()
                temp = line.strip().split(',')  # 扒皮
                flag_list_process.sort()
                flag_list.sort()
                tbar.update()
                if flag_list_process == flag_list:  #  排序后比较
                    all_dict = dataBlock2Sql(buffer)
                    mydb.writein('BASIC'+date, all_dict)
                    buffer = []
                    flag_list_process = []
    print(0)

