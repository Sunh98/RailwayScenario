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
        if flag not in flag_list and flag != 'GRS':
            flag_list.append(flag)
    return flag_list

def dataBlock2Sql(buffer, *args):
    all_dict = {}
    basic_dict = {}
    azi_dict = {}
    ele_dict = {}
    snr_dict = {}
    grs_dict = {}
    prn_list = []
    res_list = []
    for item in buffer:
        temp = item.strip().split(',')
        flag = temp[0][-3:]
        if flag == 'GGA':
            current_time = NmeaFunc.ReadGGA(item)['Time']
            time_stamp = NmeaFunc.ReadGGA(item)['Timestamp']
            basic_dict = dict(basic_dict, **NmeaFunc.ReadGGA(item))
        elif flag == 'RMC':
            basic_dict = dict(basic_dict, **NmeaFunc.ReadRMC(item))
        elif flag == 'GSV':
            ele_dict = dict(ele_dict, **NmeaFunc.ReadGSV(item)[0])
            azi_dict = dict(azi_dict, **NmeaFunc.ReadGSV(item)[1])
            snr_dict = dict(snr_dict, **NmeaFunc.ReadGSV(item)[2])

        elif flag == 'GRS':
            res_list.append(NmeaFunc.ReadGRS(item))
        elif flag == 'GSA':
            prn_list.append(NmeaFunc.ReadGSA(item))
    end = 0

    if len(prn_list) == 0 or len(res_list) == 0:
        pass
    elif len(prn_list) >= 5:
        pass
    else:
        for i in range(len(prn_list)):
            if i == 3:
                grs_dict['prn' + str(i)] = "'" + ','.join(prn_list[i - 1] + prn_list[i]) + "'"
                grs_dict['res' + str(i)] = "'" + ','.join(res_list[i - 1] + res_list[i]) + "'"
            else:
                grs_dict['prn' + str(i + 1)] = "'" + ','.join(prn_list[i]) + "'"
                grs_dict['res' + str(i + 1)] = "'" + ','.join(res_list[i]) + "'"
        grs_dict = dict(grs_dict, **{'Time': current_time, 'Timestamp': time_stamp})
        all_dict['grs'] = grs_dict

    snr_dict = dict(snr_dict, **{'Time': current_time, 'Timestamp': time_stamp})
    azi_dict = dict(azi_dict, **{'Time': current_time, 'Timestamp': time_stamp})
    ele_dict = dict(ele_dict, **{'Time': current_time, 'Timestamp': time_stamp})
    all_dict['basic'] = basic_dict
    all_dict['azi'] = azi_dict
    all_dict['ele'] = ele_dict
    all_dict['snr'] = snr_dict

    return all_dict

if __name__ == '__main__':
    mydb = SQL("ex220630")
    device = 'Sep'
    input_path = SelectandGet()

    mydb.create_table('BASIC'+device, NmeaFunc.BasicCol())
    mydb.create_table('AZI'+device, NmeaFunc.GsvCol(device))
    mydb.create_table('ELE' + device, NmeaFunc.GsvCol(device))
    mydb.create_table('SNR' + device, NmeaFunc.GsvCol(device))
    mydb.create_table('GRS'+device, NmeaFunc.PrnCol())
    #  计算需要处理的数据总量
    with open(input_path, encoding='utf-8') as f_in:
        #  计算需要处理的数据总量
        count = len(f_in.readlines())
        print("The number of lines of text to be processed is %d" % count)
        f_in.seek(0)   #文件指针位置归零
        #  查询数据块标志位
        flags = []
        for i in range(200):
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
            flag_1st = temp[0][-3:]
            flag_1st_gsv = [temp[0],temp[2]]
            flag = temp[0][-3:]
            while line:
                if flag not in flag_list_process and flag != 'GRS':
                    flag_list_process.append(flag)
                buffer.append(line)
                line = f_in.readline()
                temp = line.strip().split(',')  # 扒皮
                flag = temp[0][-3:]
                flag_list_process.sort()
                flag_list.sort()
                tbar.update()
                if flag_list_process == flag_list and flag == flag_1st:  #  排序后比较
                    if flag_1st == 'GSV' and flag_1st_gsv != [temp[0],temp[2]]:
                        continue
                    all_dict = dataBlock2Sql(buffer)
                    mydb.writein('BASIC'+device, all_dict['basic'])
                    mydb.writein('AZI'+device, all_dict['azi'])
                    mydb.writein('ELE' + device, all_dict['ele'])
                    mydb.writein('SNR' + device, all_dict['snr'])
                    if 'grs' in all_dict:
                        mydb.writein('GRS'+device,all_dict['grs'])
                    buffer = []
                    flag_list_process = []
    print(0)

