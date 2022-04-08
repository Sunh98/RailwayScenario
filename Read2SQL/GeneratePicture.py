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
import numpy as np
import math

def Toten(temp):
    temp = temp - 1
    if temp <= 0:
        return 0
    else:
        return temp//10



if __name__ == '__main__':
    mydb = SQL('ringway')
    date = '210612'

    sns.set_style("white")


    """data normalization"""
    snr = []
    snr_n = []
    column = mydb.getcol('snr'+date)[2:]  # all of satellite snr
    temp = mydb.readall(column, 'snr'+date, form='1D')
    for num in temp:
        if num!= None and num > 0:
            snr.append(num)
    snr = np.array(snr)
    """-------------------"""

    '''Data temporary storage area '''
    ''' list(range())
    section = list(range(447,486)) + list(range(696,737)) + list(range(1602,1647)) + list(range(1988,2017)) + list(range(2241,2282)) + list(range(2307,2351)) #urban
    section = list(range(579,606)) + list(range(936,1013)) + list(range(1311,1394)) + list(range(2137,2167)) #half 
    section = list(range(2948,2957)) + list(range(6459,6470)) + list(range(9336,9347)) #bridge
    section = list(range(4250,4309)) + list(range(7268,7319)) #station
    section = [500,550,600,650,700,750] + list(range(1100,2000,50)) + list(range(4550,5500,50)) + list(range(7550,8550,50)) # open
    '''
    ''' -------------------------- '''

    '''
    
    '''
    section = [500,550,600,650,700,750] + list(range(1100,2000,50)) + list(range(4550,5500,50)) + list(range(7550,8550,50)) # open
    for index in section:
        snr_array = np.zeros((9,36))
        snr_array.dtype = np.float
        for col in column:
            azi = mydb.readone(col,index,'azi'+date)
            ele = mydb.readone(col, index, 'ele' + date)
            snr_s = mydb.readone(col, index, 'snr' + date)
            if azi != None and ele != None and snr_s != None:
                snr_mm = (snr_s - np.min(snr)) / (np.max(snr) - np.min(snr))  # max-min normalization
                snr_array[Toten(ele), Toten(azi)] = snr_mm
        sns.heatmap(snr_array, vmax=1, vmin=0, cmap='Blues', cbar=False, square=True)
        plt.gcf().set_size_inches(8, 2)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('D:/Dataphoto/symmetry8_2/open/'+ date +'_'+str(index)+'_1.jpg')
        sns.heatmap(np.flip(snr_array,axis=1), vmax=1, vmin=0, cmap='Blues', cbar=False, square=True)
        plt.gcf().set_size_inches(8, 2)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig('D:/Dataphoto/symmetry8_2/open/'+ date +'_'+str(index)+'_2.jpg')











