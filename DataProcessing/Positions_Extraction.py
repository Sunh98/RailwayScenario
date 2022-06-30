# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario 
 @File: Positions_Extraction.py
 @IDE: PyCharm 
 @Author: Sunh98
 @Date: 2022/6/28
        14:52
 @Email: 21120240@bjtu.edu.cn

"""

from SQLFunction import SQL
import NmeaFunc
import numpy as np
import os

if __name__ == '__main__':
    mydb = SQL('lab220630')

    sql = 'select Timestamp, Lon, Lat from basicp2 where status = 4'
    mydb.cursor.execute(sql)
    result = mydb.cursor.fetchall()

    fake_pos = []
    for epoch in result:
        time_stamp = epoch[0]
        sql = 'select Lon, Lat from basicf2 where timeStamp = %d' %time_stamp
        mydb.cursor.execute(sql)
        search_result = mydb.cursor.fetchone()
        fake_pos.append(search_result)

    # true_pos = np.array(result)
    # fake_pos = np.array(fake_pos)
    path = 'pos_220630_lab.txt'
    if os.path.exists(path):
        os.remove(path)
    with open(path,'a+') as f_out:
        for true_item, fake_item in zip(result, fake_pos):
            true_item = list(map(str, true_item))
            fake_item = list(map(str, fake_item))
            string = '\t'.join(true_item) + '\t' + '\t'.join(fake_item) + '\n'
            f_out.write(string)
        f_out.close()

    print(0)