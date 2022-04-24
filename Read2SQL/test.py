# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from SQLFunction import SQL
import NmeaFunc as NF
import seaborn as sns
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import GeneratePicSQL as GPSQL
import time
import pandas as pd

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
#[696,737,447,486,2241,2282,1988,2017],[4550,4570,5000,5020,5520,5540,7550,7570,8500,8520]
if __name__ == '__main__':
    mydb = SQL('ringway')
    # section = list(range(1,9976))
    # a = GPSQL.make_matrixandplot_single(mydb, '210612', section,'210612','open')

    a = mydb.readone(['Lon','Lat'],'3','basic210612')
    name = ['real', 'predict']
    result = pd.DataFrame(columns=name, data=a)
    result.to_csv("2.csv")

    # a = GPSQL.make_matrixandplot(mydb,'220407',[111,158],'new_test')
    # snr = []
    # snr_log = []
    # mydb = SQL("testdb")
    # d = NF.GsvCol()[0][0]
    # c = mydb.getcol('svsnr')[1:]
    # a = mydb.readall(c,'svsnr',form='1D')
    # for num in a :
    #     if num != None and int(num) >=0:
    #         snr.append(int(num))
    # # snr = np.array(snr[:300])
    # sns.histplot(snr, kde = True, binwidth=5, shrink=1,stat='probability')
    #
    # print(stats.shapiro(snr[0:400]))
    #
    # print(stats.normaltest(snr[0:400]))
    # plt.savefig('D:/KK.jpg')
    # plt.show()

    print(0)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
