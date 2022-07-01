# -*- coding: UTF-8 -*-
"""
 @Project: RailwayScenario 
 @File: Cal&PlotError.py
 @IDE: PyCharm 
 @Author: Sunh98
 @Date: 2022/6/30
        10:53
 @Email: 21120240@bjtu.edu.cn

"""

import matplotlib.pyplot as plt
import numpy as np
from geopy import distance

if __name__ == '__main__':
    all_pos = np.loadtxt('pos_220629_ex.txt')
    pos_error = []
    north_error = []
    east_error = []
    time_stamps = tuple(map(int,all_pos[:,0]))
    for i in range(len(time_stamps)):
        true_pos = (all_pos[:, 2][i], all_pos[:, 1][i])
        fake_pos = (all_pos[:, 4][i], all_pos[:, 3][i])
        temp_pos = distance.distance(true_pos,fake_pos).m
        pos_error.append(temp_pos)
        temp_north = distance.distance(true_pos,(fake_pos[0],true_pos[1])).m
        if true_pos[0] > fake_pos[0]:
            north_error.append(temp_north)
        else:
            north_error.append(-temp_north)
        temp_east = distance.distance(true_pos,(true_pos[0],fake_pos[1])).m
        if true_pos[1] > fake_pos[1]:
            east_error.append(temp_east)
        else:
            east_error.append(-temp_east)
    plt.figure(1)
    plt.title('error')
    plt.plot(time_stamps, pos_error)
    plt.figure(2)
    plt.title('north error')
    plt.plot(time_stamps, north_error)
    plt.figure(3)
    plt.title('east error')
    plt.plot(time_stamps, east_error)
    plt.show()
    print(0)




