# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario
 @File: getRMSLargeThan5
 @IDE: PyCharm
 @Author: Sunh98
 @Date: 2022/5/28
        22:11
 @Email: 21120240@bjtu.edu.cn

"""
from SQLFunction import SQL

if __name__ == '__main__':

    mydb = SQL("ringway")
    sql = 'select id, alt_std from gst191217head where alt_std > 5'
    mydb.cursor.execute(sql)
    result = mydb.cursor.fetchall()
    with open('17.txt','a',encoding='utf-8') as f_in:
        for item in result:
            list1 = []
            sql = 'select Lon, Lat from basic191217head where id = %d' %item[0]
            mydb.cursor.execute(sql)
            result2 = list(mydb.cursor.fetchone())
            result2.extend([item[0], item[1]])
            list1.extend(result2)
            list1 = list(map(str, list1))
            print(list1)
            str1 = '\t'.join(list1) + '\n'
            f_in.write(str1)
        f_in.close()
    print(result)
