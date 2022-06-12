# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario
 @File: AnalyseNMEAfromF10
 @IDE: PyCharm
 @Author: Sunh98
 @Date: 2022/5/12
        16:02
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



if __name__ == '__main__':
    mydb = SQL("ringway")
    date = '210612P2'
    device = 'BD980'
    path_in = SelectandGet()
    tableList = ['BASIC'+date, 'AZI'+date, 'ELE'+date, 'SNR'+date, 'GST'+date, 'GRS'+date]
    mydb.create_table(tableList[0], NmeaFunc.BasicCol())
    # mydb.create_table(tableList[1], NmeaFunc.GsvCol())
    # mydb.create_table(tableList[2], NmeaFunc.GsvCol())
    # mydb.create_table(tableList[3], NmeaFunc.GsvCol())
    # mydb.create_table(tableList[4], NmeaFunc.GSTDict())
    # mydb.create_table(tableList[5], NmeaFunc.PrnCol())

    with open(path_in,encoding='utf-8') as f_in:
        count = len(f_in.readlines())
        print("The number of lines of text to be processed is %d" % count)
        f_in.seek(0)   #计算待处理的数据总量

        lineWithTime = ['GGA','RMC','GRS','GST']
        line = f_in.readline()
        temp = line.strip().split(',')
        flagBit_1 = temp[0][-3:]  #首标识位
        flagBit = flagBit_1
        while flagBit not in lineWithTime:  #寻找带有时间的标识位
            line = f_in.readline()
            temp = line.strip().split(',')
            flagBit = temp[0][-3:]
        startTime = temp[1]
        f_in.seek(0)   #重置文件指针

        with tqdm(range(count), desc='Text Processing: ') as tbar:
            line = f_in.readline()
            temp = line.strip().split(',')  # 扒皮
            time = startTime
            startFlag = True
            basic_dict = {}
            ele_dict  = {}
            azi_dict = {}
            snr_dict = {}
            prn_list = []
            res_list = []
            while line:
                flagBit = temp[0][-3:]
                if flagBit_1 == flagBit:
                    if startFlag:
                        startFlag = False

                    else:
                        time = current_time
                        startFlag = False
                        mydb.writein(tableList[0], basic_dict)
                        # mydb.writein(tableList[2], dict(ele_dict, **{'time': time}))
                        # mydb.writein(tableList[1], dict(azi_dict, **{'time': time}))
                        # mydb.writein(tableList[3], dict(snr_dict, **{'time': time}))
                        grs_dict = {}
                        if len(prn_list) == 0 or len(res_list) == 0:
                            pass
                        elif len(prn_list) >=5:
                            pass
                        else:
                            for i in range(len(prn_list)):
                                if i == 3:
                                    grs_dict['prn' + str(i)] = "'" + ','.join(prn_list[i-1]+prn_list[i]) + "'"
                                    grs_dict['res' + str(i)] = "'" + ','.join(res_list[i-1]+res_list[i]) + "'"
                                else:
                                    grs_dict['prn' + str(i + 1)] = "'"+','.join(prn_list[i])+"'"
                                    grs_dict['res' + str(i + 1)] = "'"+','.join(res_list[i])+"'"

                        # mydb.writein(tableList[5], dict(grs_dict, **{'time': time}))
                        prn_list = []
                        res_list = []
                if flagBit == 'GST':
                    mydb.writein(tableList[4], NmeaFunc.ReadGST(line))
                elif flagBit == 'GGA':
                    current_time = NmeaFunc.ReadGGA(line)['Time']
                    basic_dict = dict(basic_dict,**NmeaFunc.ReadGGA(line))
                elif flagBit == 'RMC':
                    basic_dict = dict(basic_dict, **NmeaFunc.ReadRMC(line))
                elif flagBit == 'GSV':
                    ele_dict = dict(ele_dict, **NmeaFunc.ReadGSV(line)[0])
                    azi_dict = dict(azi_dict, **NmeaFunc.ReadGSV(line)[1])
                    snr_dict = dict(snr_dict, **NmeaFunc.ReadGSV(line)[2])
                elif flagBit == 'GSA':
                    prn_list.append(NmeaFunc.ReadGSA(line))
                elif flagBit == 'GRS':
                    res_list.append(NmeaFunc.ReadGRS(line))
                tbar.update()
                line = f_in.readline()
                temp = line.strip().split(',')  # 扒皮


    print(0)


