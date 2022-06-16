# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario
 @File: getdata
 @IDE: PyCharm
 @Author: Sunh98
 @Date: 2022/6/1
        16:06
 @Email: 21120240@bjtu.edu.cn

"""
import NmeaFunc
from SQLFunction import SQL
import numpy as np

def pad_or_truncate(some_list, target_len):
    return some_list[:target_len] + [0]*(target_len - len(some_list))

if __name__ == '__main__':
    mydb = SQL("ringway")
    input_list = []
    output_list = []
    for i in range(50000,70001):  #50000,70001   2527,32528

        input_epoch = []
        sql = 'select time from grs210612f10 where id = %d' %i
        mydb.cursor.execute(sql)
        time = mydb.cursor.fetchone()[0]
        if time[time.rfind('.')+1:] != '00':
            continue
        sql = 'select prn1,prn2,prn3 from grs210612f10 where id = %d' % i
        mydb.cursor.execute(sql)
        prn_list = mydb.cursor.fetchone()
        sql = 'select res1,res2,res3 from grs210612f10 where id = %d' % i
        mydb.cursor.execute(sql)
        res_list = mydb.cursor.fetchone()

        sql = 'select Lon, Lat from basic210612f10 where time = %s' % ("'"+time+"'")
        mydb.cursor.execute(sql)
        pos_train = np.array(mydb.cursor.fetchone())

        sql = 'select Lon, Lat from basic210612p2 where time = %s' % ("'"+time+"'")
        mydb.cursor.execute(sql)
        pos_true = np.array(mydb.cursor.fetchone())
        if pos_true is None:
            pass
        print(time,pos_train, pos_true)
        # delta_pos = list((pos_true - pos_train)*100000)
        output_list.append(list(pos_true)+list(pos_train))

        prn_gp = prn_list[0].split(',')
        prn_gl = prn_list[1].split(',')
        prn_gb = prn_list[2].split(',')
        res_gp = res_list[0].split(',')
        res_gl = res_list[1].split(',')
        res_gb = res_list[2].split(',')

        for index, item in enumerate(prn_gp):
            if len(item)<2:
                item = item.zfill(2)
            sql = 'select %s from azi210612f10 where id = %d' % ('GP' + item, i)
            mydb.cursor.execute(sql)
            azi = mydb.cursor.fetchone()[0]/360
            sql = 'select %s from ele210612f10 where id = %d' % ('GP' + item, i)
            mydb.cursor.execute(sql)
            ele = mydb.cursor.fetchone()[0]/90
            input_epoch.extend([float(res_gp[index]),azi,ele])
        for index, item in enumerate(prn_gl):
            if len(item)<2:
                item = item.zfill(2)
            sql = 'select %s from azi210612f10 where id = %d' % ('GL' + item, i)
            mydb.cursor.execute(sql)
            azi = mydb.cursor.fetchone()[0]/360
            sql = 'select %s from ele210612f10 where id = %d' % ('GL' + item, i)
            mydb.cursor.execute(sql)
            ele = mydb.cursor.fetchone()[0]/90
            input_epoch.extend([float(res_gl[index]),azi,ele])
        for index, item in enumerate(prn_gb):
            if len(item)<2:
                item = item.zfill(2)
            sql = 'select %s from azi210612f10 where id = %d' % ('GB' + item, i)
            mydb.cursor.execute(sql)
            azi = mydb.cursor.fetchone()[0]/360
            sql = 'select %s from ele210612f10 where id = %d' % ('GB' + item, i)
            mydb.cursor.execute(sql)
            ele = mydb.cursor.fetchone()[0]/90
            input_epoch.extend([float(res_gb[index]),azi,ele])
        input_epoch = pad_or_truncate(input_epoch,100)
        input_list.append(input_epoch)

    input_list = np.array(input_list)
    output_list = np.array(output_list)
    np.savetxt('validfea.txt', input_list, fmt='%.3f')
    np.savetxt('posall.txt', output_list, fmt='%.10f')





