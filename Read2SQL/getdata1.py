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
"""
特征在处理后再进行补0，整体的排列方式
The features are processed and then complemented by 0. The overall arrangement
"""

import NmeaFunc
from SQLFunction import SQL
import numpy as np

def pad_or_truncate(some_list, target_len, value_in):
    return some_list[:target_len] + [value_in]*(target_len - len(some_list))

def padList(res_list, list_length, azi_list, ele_list, snr_list):
    res_list_abs = list(map(abs, res_list))  # 数据绝对值
    index = res_list_abs.index(min(res_list_abs))  #最小值的索引
    res_value = res_list[index]
    azi_value = azi_list[index]
    ele_value = ele_list[index]
    snr_value = snr_list[index]
    res_list = pad_or_truncate(res_list, list_length, res_value)
    azi_list = pad_or_truncate(azi_list, list_length, azi_value)
    ele_list = pad_or_truncate(ele_list, list_length, ele_value)
    snr_list = pad_or_truncate(snr_list, list_length, snr_value)

    return res_list + azi_list + ele_list + snr_list




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

        # sql = 'select Lon, Lat from basic210612f10 where time = %s' % ("'"+time+"'")
        # mydb.cursor.execute(sql)
        # pos_train = np.array(mydb.cursor.fetchone())
        #
        # sql = 'select Lon, Lat from basic210612p2 where time = %s' % ("'"+time+"'")
        # mydb.cursor.execute(sql)
        # pos_true = np.array(mydb.cursor.fetchone())
        # if pos_true is None:
        #     pass
        # print(time,pos_train, pos_true)
        # # delta_pos = list((pos_true - pos_train)*100000)
        # output_list.append(list(pos_true)+list(pos_train))

        prn_gp = prn_list[0].split(',')
        prn_gl = prn_list[1].split(',')
        prn_gb = prn_list[2].split(',')
        res_gp = res_list[0].split(',')
        res_gl = res_list[1].split(',')
        res_gb = res_list[2].split(',')

        allres = []  # All of parameters list in each epoch.
        allazi = []
        allele = []
        allsnr = []

        allres = res_gp + res_gl + res_gb
        allres = list(map(float,allres))


        for index, item in enumerate(prn_gp):
            if len(item)<2:
                item = item.zfill(2)
            sql = 'select %s from azi210612f10 where id = %d' % ('GP' + item, i)
            mydb.cursor.execute(sql)
            azi = mydb.cursor.fetchone()[0]/360
            sql = 'select %s from ele210612f10 where id = %d' % ('GP' + item, i)
            mydb.cursor.execute(sql)
            ele = mydb.cursor.fetchone()[0]/90
            sql = 'select %s from snr210612f10 where id = %d' % ('GP' + item, i)
            mydb.cursor.execute(sql)
            snr = mydb.cursor.fetchone()[0] / 55
            allazi.append(azi)
            allele.append(ele)
            allsnr.append(snr)
        for index, item in enumerate(prn_gl):
            if len(item)<2:
                item = item.zfill(2)
            sql = 'select %s from azi210612f10 where id = %d' % ('GL' + item, i)
            mydb.cursor.execute(sql)
            azi = mydb.cursor.fetchone()[0]/360
            sql = 'select %s from ele210612f10 where id = %d' % ('GL' + item, i)
            mydb.cursor.execute(sql)
            ele = mydb.cursor.fetchone()[0]/90
            sql = 'select %s from snr210612f10 where id = %d' % ('GL' + item, i)
            mydb.cursor.execute(sql)
            snr = mydb.cursor.fetchone()[0] / 55
            allazi.append(azi)
            allele.append(ele)
            allsnr.append(snr)
        for index, item in enumerate(prn_gb):
            if len(item)<2:
                item = item.zfill(2)
            sql = 'select %s from azi210612f10 where id = %d' % ('GB' + item, i)
            mydb.cursor.execute(sql)
            azi = mydb.cursor.fetchone()[0]/360
            sql = 'select %s from ele210612f10 where id = %d' % ('GB' + item, i)
            mydb.cursor.execute(sql)
            ele = mydb.cursor.fetchone()[0]/90
            sql = 'select %s from snr210612f10 where id = %d' % ('GB' + item, i)
            mydb.cursor.execute(sql)
            snr = mydb.cursor.fetchone()[0] / 55
            allazi.append(azi)
            allele.append(ele)
            allsnr.append(snr)



        input_epoch = padList(allres, 30, allazi, allele, allsnr)
        input_list.append(input_epoch)

    input_list = np.array(input_list)
    # output_list = np.array(output_list)
    np.savetxt('validfea3.txt', input_list, fmt='%.3f')
    # np.savetxt('posall.txt', output_list, fmt='%.10f')





