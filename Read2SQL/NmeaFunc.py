# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario 
 @File: NmeaFunc.py.py
 @IDE: PyCharm 
 @Author: Sunh98
 @Date: 2022/4/1
        17:27
 @Email: 21120240@bjtu.edu.cn

"""

import os
import sys

def Prn(kind):
    kind.upper()
    GPS = ['GP' +'%.2d ' %i for i in range(1 ,31)]
    BDS = ['GB' +'%.2d ' %i for i in range(1 ,61)]
    GLO = ['GL' +'%.2d ' %i for i in range(61 ,96)]
    GAL = ['GA' +'%.2d ' %i for i in range(61 ,96)]
    if kind == 'GPS':
        return GPS
    elif kind == 'BDS':
        return BDS
    elif kind == 'GLO':
        return GLO
    elif kind == 'GAL':
        return GAL
    else:
        return None

def BasicCol() ->tuple :
    """
    tuple[0] is column; tuple[1] is column_type
    """
    col = ['Date','Lon','Lat','Speed','Course','SU',
           'HDOP','PDOP','VDOP','Height','Dis','VetDis','AlgDis']
    col_type = ['char(20)','float(20,15)','float(20,15)','double','double','int',
                'double','double','double','double','float','float','float']
    return (col,col_type)

def GsvCol() ->tuple :
    """
       GPS, BDS, GLO, GAL.
       kind is the system of GNSS
       tuple[0] is column; tuple[1] is column_type
    """
    kind = ['GPS','BDS','GLO','GAL']
    col = []
    col_type = []
    for item in kind:
        col.extend(Prn(item))
    col_type = ['int' for _ in col]
    return (col,col_type)

def addtimeP2(file_path:str)->str:
    """add time flag to the nmea data"""
    file_outputpath = file_path[:-4]+'_addtime.txt'

    """file operations block"""
    if os.path.exists(file_outputpath):
        command = str(input("File is exist, Do you want to delete it and recreate it? (Y/n)\n")).upper()
        if  command == 'Y':
            os.remove(file_outputpath)
        elif command == 'N':
            print('Cancel the operation!\n')
            sys.exit()
        else:
            print('Error: You entered a wrong command!\n ')
            sys.exit()
    else:
        print('File is not exist, will create one\n ')


    with open(file_path, encoding='utf-8') as f_in:
        with open(file_outputpath, 'a', encoding='utf-8') as f_out:
            line = f_in.readline()
            temp = line.strip().split(',')  #扒皮
            while not [x for x in temp if 'RMC' in x]:  #从第一个RMC语句开始插时间戳
                line = f_in.readline()
                temp = line.strip().split(',')
            time = temp[1][0:temp[1].rfind('.')]  #读第一个RMC的时间戳
            temp.insert(0, time)
            nmealine = ','.join(temp) + '\n'
            f_out.write(nmealine)
            line = f_in.readline()
            temp = line.strip().split(',')
            while line:
                if any([x for x in temp if 'RMC' in x]):  # 是RMC更新时间戳
                    time = temp[1][0:temp[1].rfind('.')]
                    temp.insert(0, time)  # 在每行数据流前加入时间戳，方便辨识
                else:      #不是RMC的都打标签
                    temp.insert(0,time)
                nmealine = ','.join(temp) + '\n'
                f_out.write(nmealine)
                line = f_in.readline()
                temp = line.strip().split(',')
            f_out.close()
            print("Success: Have been added time flag!")
    return file_outputpath


