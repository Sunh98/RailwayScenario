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


def ReadGST(nmea_stmt):
    """
    smjr_std == Standard deviation of semi-major axis of error ellipse (m)
    smnr_std == Standard deviation of semi-minor axis of error ellipse (m)
    orient   == Standard deviation of semi-minor axis of error ellipse (m)
    lat_std  == Standard deviation of latitude error (m)
    lon_std  == Standard deviation of longitude error (m)
    alt_std  == Standard deviation of altitude error (m)

    Example:
         (GPS only)
        $GPGST,141451.00,1.18,0.00,0.00,0.0000,0.00,0.00,0.00*6B
         (Combined GPS and GLONASS)
        $GNGST,143333.00,7.38,1.49,1.30,68.1409,1.47,1.33,2.07*4A
    """
    nmea_list = nmea_stmt.strip().split(',')
    nmea_dit = {}
    nmea_dit['alt_std'] = float(nmea_list[-1][:nmea_list[-1].rfind('*')])
    nmea_dit['lon_std'] = float(nmea_list[-2])
    nmea_dit['lat_std'] = float(nmea_list[-3])
    nmea_dit['orient'] = float(nmea_list[-4])
    nmea_dit['smnr_std'] = float(nmea_list[-5])
    nmea_dit['smjr_std'] = float(nmea_list[-6])
    nmea_dit['rms'] = float(nmea_list[-7])
    nmea_dit['utc'] = nmea_list[-8]

    return nmea_dit

class NMEA:
    "A nmea data operations"
    def __init__(self, database=''):
        if database == '':
            pass
        else:
            self.database = database









def Prn(kind):
    kind.upper()
    GPS = ['GP' +'%.2d ' %i for i in range(1 ,33)]
    GBS = ['GB' +'%.2d ' %i for i in range(1 ,65)]
    GLO = ['GL' +'%.2d ' %i for i in range(60 ,99)]
    GAL = ['GA' +'%.2d ' %i for i in range(1 ,40)]
    GQ  = ['GQ' +'%.2d ' %i for i in range(90 ,100)]
    if kind == 'GPS':
        return GPS
    elif kind == 'GBS':
        return GBS
    elif kind == 'GLO':
        return GLO
    elif kind == 'GAL':
        return GAL
    elif kind == 'GQ':
        return GQ
    else:
        return None

def BasicCol() ->tuple :
    """
    tuple[0] is column; tuple[1] is column_type
    """
    col = ['Date','Lon','Lat','Speed','Course','SU','status',
           'HDOP','PDOP','VDOP','Height','Dis','VetDis','AlgDis','clf',
            ]
    col_type = ['char(20)','double','double','double','double','int','int',
                'double','double','double','double','float','float','float','char(20)',
                'float','float','float','float','float','float']
    return (col,col_type)

def GsvCol(GB = 'GB') ->tuple :
    """
       GPS, BDS, GLO, GAL.
       kind is the system of GNSS
       tuple[0] is column; tuple[1] is column_type
    """
    kind = ['GPS','GBS','GLO','GAL','GQ']
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


def spangetnmea(file_path:str):
    file_outputpath = file_path[:file_path.rfind('.')] + '_new.txt'

    """file operations block"""
    if os.path.exists(file_outputpath):
        command = str(input("File is exist, Do you want to delete it and recreate it? (Y/n)\n")).upper()
        if command == 'Y':
            os.remove(file_outputpath)
        elif command == 'N':
            print('Cancel the operation!\n')
            sys.exit()
        else:
            print('Error: You entered a wrong command!\n ')
            sys.exit()
    else:
        print('File is not exist, will create one\n ')

    with open(file_path,encoding='utf-8') as f_in:
        with open(file_outputpath, 'a', encoding='utf-8') as f_out:
            line = f_in.readline()
            temp = line.strip().split(',')
            while line:
                if '$' in temp[0]:
                    f_out.write(line)
                line = f_in.readline()
                temp = line.strip().split(',')
            f_out.close()
    return file_outputpath






