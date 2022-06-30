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
    all_pos = np.loadtxt('pos_220630_lab.txt')
    pos_error = []
    time_stamps = tuple(map(int,all_pos[:,0]))
    for i in range(len(time_stamps)):
        true_pos = (all_pos[:, 2][i], all_pos[:, 1][i])
        fake_pos = (all_pos[:, 4][i], all_pos[:, 3][i])
        temp = distance.distance(true_pos,fake_pos).m
        pos_error.append(temp)

    plt.plot(time_stamps, pos_error)
    plt.show()
    print(0)




