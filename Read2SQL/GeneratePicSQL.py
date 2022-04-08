# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario 
 @File: GeneratePicSQL.py
 @IDE: PyCharm 
 @Author: Sunh98
 @Date: 2022/4/7
        20:36
 @Email: 21120240@bjtu.edu.cn

"""
from SQLFunction import SQL
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def Toten(temp):
    temp = temp - 1
    if temp <= 0:
        return 0
    else:
        return temp//10

def normalization(array, value, mode = 'max_min'):
    '''
    array must be a 1D array
    mode can be max_min
    '''
    if mode == 'max_min':
        mm = (value - np.min(array)) / (np.max(array) - np.min(array))
        return mm
    elif mode == 'z_score':
        zs = (value - np.mean(array)) / np.std(array)
        return zs

def make_matrixandplot(database, date, section, path, classficaiton = None):
    '''
    section can be a list or tuple, form is [start,end,...,start,end]
    '''



    snrall = []
    column = database.getcol('snr' + date)[2:]  # all of satellite snr
    temp = database.readall(column, 'snr' + date, form='1D')
    for num in temp:
        if num!= None and num > 0:
            snrall.append(num)
    snrall = np.array(snrall)

    allsection = []
    for i, item in enumerate(section):
        if i % 2 == 0:
            start = item
        elif i % 2 == 1:
            end = item
            allsection.extend(list(range(start, end)))

    column = database.getcol('snr' + date)[2:]
    for index in allsection:
        snr_array = np.zeros((9, 36))
        snr_array.dtype = float
        for col in column:
            azi = database.readone(col, index, 'azi'+date)
            ele = database.readone(col, index, 'ele'+date)
            snr = database.readone(col, index, 'snr'+date)
            if azi != None and ele != None and snr != None:
                snr_norm = normalization(snrall,snr,'z_score')
                snr_array[Toten(ele), Toten(azi)] = snr_norm
        if classficaiton == None:
            clf = database.readone('clf', index, 'basic'+date)
            make_plot(snr_array, index, date, path, clf)
        else:
            make_plot(snr_array, index, date, path, classficaiton)



def make_plot(snr_array, index, date, path, clf):
    sns.heatmap(snr_array, vmax=1, vmin=-1, cmap='Blues', cbar=False, square=True)
    plt.gcf().set_size_inches(8, 2)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('D:/Dataphoto/'+path+'/'+clf+'/'+date+'_'+str(index)+'.jpg')
    print('Finished {} {}.jpg'.format(clf, index))










