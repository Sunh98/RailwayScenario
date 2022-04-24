# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario 
 @File: WriteIntoDatabase.py
 @IDE: PyCharm 
 @Author: Sunh98
 @Date: 2022/4/1
        14:37
 @Email: 21120240@bjtu.edu.cn

"""
from SQLFunction import SQL
import NmeaFunc

if __name__ == '__main__':
    mydb = SQL("ringway")
    date = '201206'
    mydb.create_table('BASIC'+date, NmeaFunc.BasicCol()[0], NmeaFunc.BasicCol()[1])

    #create a basic table
    mydb.create_table('AZI'+date, NmeaFunc.GsvCol('BD')[0], NmeaFunc.GsvCol()[1])
    mydb.create_table('ELE'+date, NmeaFunc.GsvCol('BD')[0], NmeaFunc.GsvCol()[1])
    mydb.create_table('SNR'+date, NmeaFunc.GsvCol('BD')[0], NmeaFunc.GsvCol()[1])
    mydb.nmea2sql("222.txt", date)


    print(0)




