# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario 
 @File: GeneratePicture.py
 @IDE: PyCharm 
 @Author: Sunh98
 @Date: 2022/4/6
        20:29
 @Email: 21120240@bjtu.edu.cn

"""

from SQLFunction import SQL
import NmeaFunc
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    mydb = SQL('ringway')
    date = '220117'
    """数据标准化"""
    snr = []
    col = mydb.getcol('snr'+date)[2:]
    temp = mydb.readall(col, 'snr'+date, form='1D')
    for num in temp:
        if num!= None and num > 0:
            snr.append(num)
    sns.histplot(snr, kde=True, binwidth=5, shrink=1, stat='probability')
    plt.show()









