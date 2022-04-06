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
    # mydb.create_table('BASIC220307', NmeaFunc.BasicCol()[0], NmeaFunc.BasicCol()[1])
    #
    # #create a basic table
    # mydb.create_table('AZI220307', NmeaFunc.GsvCol()[0], NmeaFunc.GsvCol()[1])
    # mydb.create_table('ELE220307', NmeaFunc.GsvCol()[0], NmeaFunc.GsvCol()[1])
    # mydb.create_table('SNR220307', NmeaFunc.GsvCol()[0], NmeaFunc.GsvCol()[1])
    mydb.nmea2sql(NmeaFunc.addtimeP2('单点定位.txt'), '220307')



    print(0)




