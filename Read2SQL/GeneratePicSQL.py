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
from scipy.interpolate import griddata
import time

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
    elif mode == '60_max':
        m6 = (value - 0) / (60-0)
        return m6

def interp(arr, method = 'cubic'):
    X,Y = np.nonzero(arr)
    Z = arr[X,Y]
    x,y = np.mgrid[0:arr.shape[0],0:arr.shape[1]]
    if np.size(Z) != 0:
        arr_new = griddata((X,Y), Z, (x,y), method= method)
    else:
        arr_new = arr
    return arr_new

def interpnan(arr, method = 'cubic'):
    a = np.isnan(arr)
    b = (1 - a).astype(bool)
    all = np.argwhere(b)
    X = all[:,0]
    Y = all[:,1]
    Z = arr[X,Y]
    x,y = np.mgrid[0:arr.shape[0],0:arr.shape[1]]
    if np.size(Z) != 0:
        arr_new = griddata((X,Y), Z, (x,y), method= method)
    else:
        arr_new = arr
    return arr_new

def expand(arr,len = 9):
    l_add = np.flip(arr[:,36-len:], axis = 1)
    r_add = np.flip(arr[:,:len], axis = 1)
    arr = np.c_[l_add,arr]
    arr = np.c_[arr,r_add]
    return arr

def shrink(arr,len = 9):
    arr = arr[:,len:arr.shape[1]-len]
    return arr


def matrixreshape(arr):
    l_arr = arr[:,:18]
    r_arr = arr[:,18:]
    r_arr = np.flip(r_arr, axis = 0)
    # r_arr = np.flip(r_arr, axis = 1)
    all_arr = np.r_[l_arr,r_arr]
    return all_arr


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
        snr_pos = np.zeros(9, 36)
        snr_array.dtype = float
        for col in column:
            azi = database.readone(col, index, 'azi'+date)
            ele = database.readone(col, index, 'ele'+date)
            snr = database.readone(col, index, 'snr'+date)
            if azi != None and ele != None and snr != None:
                if snr > 0:
                    snr_norm = normalization(snrall,snr,'60_max')
                    snr_array[Toten(ele), Toten(azi)] = (snr_array[Toten(ele), Toten(azi)]*snr_pos[Toten(ele), Toten(azi)] + snr_norm)/(snr_pos[Toten(ele), Toten(azi)]+1)
                    print(snr_array[Toten(ele), Toten(azi)])
                    snr_array[Toten(ele), Toten(azi)] = snr_array[Toten(ele), Toten(azi)]+1
        if classficaiton == None:
            clf = database.readone('clf', index, 'basic'+date)
            make_plot(snr_array, index, date, path, clf)
        else:
            make_plot(snr_array, index, date, path, classficaiton)



def make_plot(snr_array, index, date, path, clf):
    plt.figure()
    sns.heatmap(snr_array, vmax=1, vmin=0, cmap='hot_r', cbar=False, square=True)
    plt.gcf().set_size_inches(4, 4)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('D:/Dataphoto/'+path+'/'+clf+'/'+date+'_'+str(index)+'.jpg')
    print('Finished {} {}.jpg'.format(clf, index))
    plt.close()

def make_matrixandplot_single(database, date, section, path, classficaiton = None):
    '''
    section can be a list or tuple, form is [point,point,...,point]
    '''



    # snrall = []
    # column = database.getcol('snr' + date)[2:]  # all of satellite snr
    # temp = database.readall(column, 'snr' + date, form='1D')
    # for num in temp:
    #     if num!= None and num > 0:
    #         snrall.append(num)
    # snrall = np.array(snrall)

    # allsection = []
    # for i, item in enumerate(section):
    #     if i % 2 == 0:
    #         start = item
    #     elif i % 2 == 1:
    #         end = item
    #         allsection.extend(list(range(start, end)))

    column = database.getcol('snr' + date)[2:]
    for index in section:
        start = time.perf_counter()
        snr_array = np.zeros((9, 36))
        snr_pos = np.zeros((9, 36))
        snr_array.dtype = float
        snr_result = []
        for col in column:

            azi = database.readone(col, index, 'azi' + date)
            ele = database.readone(col, index, 'ele' + date)
            snr = database.readone(col, index, 'snr' + date)
            if azi != None and ele != None and snr != None:
                if int(snr) > 0:
                    snr_result.append([azi,ele,snr])
                    snr_norm = normalization([], snr, '60_max')
                    snr_array[Toten(ele), Toten(azi)] = (snr_array[Toten(ele), Toten(azi)] * snr_pos[
                        Toten(ele), Toten(azi)] + snr_norm) / (snr_pos[Toten(ele), Toten(azi)] + 1)
                    snr_pos[Toten(ele), Toten(azi)] = snr_pos[Toten(ele), Toten(azi)] + 1
        snr_array = expand(snr_array)
        snr_array = interp(snr_array)
        snr_array = shrink(snr_array)
        snr_array = matrixreshape(snr_array)
        snr_array = interpnan(snr_array)

        if classficaiton == None:
            clf = database.readone('clf', index, 'basic' + date)
            make_plot(snr_array, index, date, path, clf)
        else:
            make_plot(snr_array, index, date, path, classficaiton)
        end = time.perf_counter()
        print(str(end - start))
    database.close()








