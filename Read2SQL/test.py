# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from SQLFunction import SQL
import NmeaFunc
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # NmeaFunc.addtimeP2('伪距差分.txt')
    mydb = SQL(database='ringway')
    a = mydb.readone('Lon',2,'basic220307')
    b = mydb.readall('GB14','SVSNR')
    #mydb.create_table('kk',['Time','Date'],['char(20)','char(20)'])
    mydb.writein('kk',['Time','Date'],['20','20'])
    c = NmeaFunc.GsvCol()

    print(c[0][0])
    print(0)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
