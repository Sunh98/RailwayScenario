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
import datetime

def sixty2ten(data_input):
    if not data_input:
        return -1
    else:
        for i in range(len(data_input)):
            Ndeg=data_input[0:(data_input.rfind(".")-2)]
            Nmin=data_input[(data_input.rfind(".")-2):-1]
            N=int(Ndeg)+float(Nmin)/60
        return N

def str2float(string):
    if not string:
        return -1.0
    if string:
        return float(string)

def str2int(string):
    if not string:
        return 0
    if string:
        if '*' in string:
            temp = string[:string.rfind('*')]
            if not temp:
                return 0
            else:
                return int(temp)
        else:
            return int(string)

def standard_time(time_str):
    if not time_str:
        return 'NULL'
    else:
        H = int(time_str[0:2])
        M = int(time_str[2:4])
        S = int(time_str[4:6])
        ss = int(time_str[7:]) * 10000
        return '"'+datetime.time(H,M,S,ss).strftime("%H:%M:%S.%f")[:-4]+'"'

def timeStampConvert(time_str):  #  以0.1s为1，计算时间戳
    if not time_str:
        return 'NULL'
    else:
        ss = int(time_str[7:8])
        s = int(time_str[4:6])*10
        m = int(time_str[2:4])*60*10
        h = int(time_str[0:2])*60*60*10
        time_stamp = h + m + s + ss
        return time_stamp


def GSTDict() -> dict:
    """
        smjr_std == Standard deviation of semi-major axis of error ellipse (m)
        smnr_std == Standard deviation of semi-minor axis of error ellipse (m)
        orient   == Standard deviation of semi-minor axis of error ellipse (m)
        lat_std  == Standard deviation of latitude error (m)
        lon_std  == Standard deviation of longitude error (m)
        alt_std  == Standard deviation of altitude error (m)
    """

    diction = {}
    column = ['alt_std', 'lon_std', 'lat_std', 'orient',
              'smnr_std', 'smjr_std', 'rms', 'utc']
    column_type = ['float', 'float', 'float', 'float',
                   'float', 'float', 'float', 'varchar(20)']
    for key, value in zip(column,column_type):
        diction[key] = value
    return diction

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
    nmea_dit['alt_std'] = str2float(nmea_list[-1][:nmea_list[-1].rfind('*')])
    nmea_dit['lon_std'] = str2float(nmea_list[-2])
    nmea_dit['lat_std'] = str2float(nmea_list[-3])
    nmea_dit['orient'] = str2float(nmea_list[-4])
    nmea_dit['smnr_std'] = str2float(nmea_list[-5])
    nmea_dit['smjr_std'] = str2float(nmea_list[-6])
    nmea_dit['rms'] = str2float(nmea_list[-7])

    nmea_dit['utc'] = standard_time(nmea_list[-8])
    return nmea_dit

def ReadGGA(nmea_stmt):
    diction = {}
    temp = nmea_stmt.strip().split(',')
    diction['Lon'] = sixty2ten(temp[4])
    diction['Lat'] = sixty2ten(temp[2])
    diction['status'] = str2int(temp[6])
    diction['SU'] = str2int(temp[7])
    diction['HDOP'] = str2float(temp[8])
    diction['height'] = str2float(temp[9])
    diction['Time'] = standard_time(temp[1])
    diction['Timestamp'] = timeStampConvert(temp[1])
    return diction

def ReadRMC(nmea_stmt):
    diction = {}
    temp = nmea_stmt.strip().split(',')
    diction['Lon'] = sixty2ten(temp[5])
    diction['Lat'] = sixty2ten(temp[3])
    diction['speed'] = str2float(temp[7])
    diction['course'] = str2float(temp[8])
    diction['Date'] = temp[9]
    return diction

def ReadGSV(nmea_stmt):
    diction_ele = {}
    diction_azi = {}
    diction_snr = {}
    temp = nmea_stmt.strip().split(',')
    GNSSsystem = GnssName(temp[0][1:3])
    i = 4
    while(i < len(temp)):
        if i % 4 == 0:
            prn = temp[i]
            if len(prn) == 1:
                prn = prn.zfill(2)
            elif len(prn) == 0:
                i = i+4
                continue
            diction_ele[GNSSsystem + prn] = str2int(temp[i + 1])
            diction_azi[GNSSsystem + prn] = str2int(temp[i + 2])
            diction_snr[GNSSsystem + prn] = str2int(temp[i + 3])
        i = i + 4
    return diction_ele, diction_azi, diction_snr

def ReadGSA(nmea_stmt)->list:
    temp = nmea_stmt.strip().split(',')
    new_temp = temp[3:-3]
    list1 = []
    for item in new_temp:
        if item == '':
            break
        else:
            list1.append(item)
    if len(list1) == 0:
        return ['null']
    else:
        return list1

def ReadGRS(nmea_stmt)->list:
    temp = nmea_stmt.strip().split(',')
    new_temp = temp[3:]
    list1 = []
    if '*' in new_temp[-1]:
        new_temp[-1] = new_temp[-1][:new_temp[-1].rfind('*')]
    for item in new_temp:
        if item == '':
            break
        else:
            list1.append(item)
    if len(list1) == 0:
        return ['null']
    else:
        return list1


class NMEA:
    "A nmea data operations"
    def __init__(self, database=''):
        if database == '':
            pass
        else:
            self.database = database





def GnssName(gnss_name):
    if gnss_name == 'BD':
        gnss_name = 'GB'
    elif gnss_name == 'QZ':
        gnss_name = 'GQ'
    else:
        pass
    return gnss_name



def Prn(kind, device):
    kind.upper()
    if device == 'Xpro':
        GPS = ['GP'+'%.2d' %i for i in range(1, 32)]
        GBS = ['GB'+'%.2d' %i for i in range(140 ,199)]
        GLO = ['GL'+'%.2d' %i for i in range(35, 65)]
        GAL = ['GA' +'%.2d ' %i for i in range(1 ,40)]
        GQ = ['GQ' +'%.2d ' %i for i in range(190 ,199)]
    elif device == 'Sep':
        GPS = ['GP' + '%.2d' % i for i in range(1, 32)]
        GBS = ['GB' + '%.2d' % i for i in range(1, 63)]
        GLO = ['GL' + '%.2d' % i for i in range(35, 65)]
        GAL = ['GA' + '%.2d ' % i for i in range(1, 40)]
        GQ = ['GQ' + '%.2d ' % i for i in range(190, 199)]
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

def BasicCol() ->dict :
    """
    tuple[0] is column; tuple[1] is column_type
    """
    diction = {}
    col = ['Time','Timestamp','Date','Lon','Lat','Speed','Course','SU','status',
           'HDOP','PDOP','VDOP','Height','Dis','VetDis','AlgDis','clf',
            ]
    col_type = ['char(20)','int','char(20)','double','double','double','double','int','int',
                'double','double','double','double','float','float','float','char(20)',
                'float','float','float','float','float','float']
    for key, value in zip(col,col_type):
        diction[key] = value
    return diction

def GsvCol(device) ->dict :
    """
       GPS, BDS, GLO, GAL.
       kind is the system of GNSS
       tuple[0] is column; tuple[1] is column_type
    """
    diction = {}
    kind = ['GPS','GBS','GLO','GAL','GQ']
    col = ['Time','Timestamp']
    col_type = []
    for item in kind:
        col.extend(Prn(item,device))
    col_type = ['int' for _ in col]
    col_type[0] = 'char(20)'
    col_type[1] = 'int'
    for key, value in zip(col, col_type):
        diction[key] = value
    return diction

def PrnCol()->dict:
    diction = {'time':'char(20)', 'Timestamp':'int'}
    diction['prn1'] = 'char(100)'
    diction['res1'] = 'char(200)'
    diction['prn2'] = 'char(100)'
    diction['res2'] = 'char(200)'
    diction['prn3'] = 'char(100)'
    diction['res3'] = 'char(200)'
    diction['prn4'] = 'char(100)'
    diction['res4'] = 'char(200)'
    return diction


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






