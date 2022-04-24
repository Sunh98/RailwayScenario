import pymysql
from itertools import chain
import sys

def sixty2ten(data_input):
    for i in range(len(data_input)):
        Ndeg=data_input[0:(data_input.rfind(".")-2)]
        Nmin=data_input[(data_input.rfind(".")-2):-1]
        N=float(Ndeg)+float(Nmin)/60
    print(N)
    return N

def str2float(string):
    if not string:
        return -1.0
    if string:
        return float(string)

def str2int(string):
    if not string:
        return -1
    if string:
         return int(string)

def removeNone(list1):
    while '' in list1:
        list1.remove('')
    return list1


class SQL:
    """This is for log on a MySQL database and other operations.
       It needs host,user,password,database
    """

    def __init__(self, database, host='localhost', user='root', password='admin'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        try:
            db = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            """Method of cursor() to get a cursor for the search of SQL"""
            cursor = db.cursor()

            self.db = db
            self.cursor = cursor
            print('Success: connect to the %s database' % self.database)
        except:
            print('Error: unable to connect database')

    def readone(self, column, index, table):
        if isinstance(column,str):
            type = 'str'
            sql = 'select %s from %s where id = %d' %(column, table, index)
        else:
            col = ','.join(column)
            sql = 'select %s from %s where clf = %s' % (col, table, index)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except:
            print('Error: unable to fetch data')

    def readall(self, column, table, form = '2D'):#column can be str or list
        type = None
        if isinstance(column,str):
            type = 'str'
            sql = 'select %s from %s' %(column, table)
        else:
            col = ','.join(column)
            sql = 'select %s from %s' % (col, table)
        try:
            self.cursor.execute(sql)
            """convert 2D tuple to 1D list"""
            """ (('20',),('None',)) -->  ['20',None]  """
            result = self.cursor.fetchall()
            if type == 'str':
                result = [element[0] for element in result]
            if form == '1D':
                result = list(chain.from_iterable(result))
            return result
        except:
            print('Error: unable to fetch data')

    def readall2(self, column:list, table):
        col = ','.join(column)
        sql = 'select %s from %s' %(col, table)
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def create_table(self, table, column:list, column_type:list):
        sql_column = ''
        for col, coltype in zip(column, column_type):
            sql_column = sql_column + str(col) + ' ' + str(coltype) + ','
        sql_column = sql_column[:-1]
        sql = 'create table %s (id INT AUTO_INCREMENT PRIMARY KEY, Time char(20), ' + sql_column + ')'
        sql = sql%table
        # print(sql)
        try:
            self.cursor.execute(sql)
            print('Success: you have created a new table of %s' %table)
        except pymysql.err.OperationalError:
            command = str(input("Table is exist, Do you want to delete it and recreate it? (Y/n)\n")).upper()
            if command == 'Y':
                self.cursor.execute("DROP TABLE IF EXISTS %s" %table)
                self.cursor.execute(sql)
                print('Success: you have replace the table of %s' %table)
            else:
                print('Cancel the operation!\n')
                sys.exit()
        except:
            print('Fail: it may have other error')

    def writein(self, table, column:list, value:list):
        """This function is used for write data into table"""
        str1 = ''
        str2 = ''
        for col, val in zip(column,value):
            str1 = str1 + str(col) + ','
            str2 = str2 + str(val) + ','
        str1 = str1[:-1]
        str2 = str2[:-1]
        sql = 'insert into %s (%s) value (%s)'%(table,str1,str2)
        print(sql)
        self.cursor.execute(sql)
        try:
            self.db.commit()
        except:
            self.db.rollback()

    def nmea2sql(self,file_path:str,get_date:str):
        with open(file_path, encoding='utf-8') as f_in:
            date = get_date
            speed = 0
            course = 0
            line = f_in.readline()
            temp = line.strip().split(',')
            time = temp[0]
            while line:
                prn = ['Time']
                azi = [time]
                ele = [time]
                snr = [time]
                while time == temp[0]:
                    if 'RMC' in temp[1] and temp[3] == 'A':
                        lon = sixty2ten(temp[6])
                        lat = sixty2ten(temp[4])
                        speed = str2float(temp[8])
                        course = str2float(temp[9])
                        date = temp[10]
                        time = temp[0]
                    elif 'GGA' in temp[1] and temp[3] != '':
                        lon = sixty2ten(temp[5])
                        lat = sixty2ten(temp[3])
                        status = int(temp[7])
                        SU = int(temp[8])
                        HDOP = str2float(temp[9])
                        height = float(temp[10])
                    elif 'GST' in temp[1]:
                        ovl = temp[4]
                        ovs = temp[5]
                        ovd = temp[6]
                        latstd = temp[7]
                        lonstd = temp[8]
                        heistd = temp[9][:temp[9].rfind('*')]
                    elif 'GSV' in temp[1] and int(temp[4]) != 0:
                        temp[-1] = temp[-1][:temp[-1].rfind('*')]
                        sys = temp[1][1:3]   #confirm the GNSS system
                        if sys == 'BD':
                            sys = 'GB'
                        temp = temp[5:]  #remove useless parts
                        for i in range(len(temp)//4):
                            temp_prn = str2int(temp[4 * i + 0])
                            if temp_prn > 100:
                                temp_prn = temp_prn - 100
                            prn.append(sys + '%.2d'%temp_prn)
                            ele.append(str2int(temp[4 * i + 1]))
                            azi.append(str2int(temp[4 * i + 2]))
                            snr.append(str2int(temp[4 * i + 3]))
                    line = f_in.readline()
                    temp = line.strip().split(',')
                col = ['Time','Date','Lon','Lat','Speed','Course','SU','status',
                       'HDOP','Height','ovl','ovs','ovd','latstd','lonstd','heistd']
                value = [time,date,lon,lat,speed,course,SU,status,
                         HDOP,height,ovl,ovs,ovd,latstd,lonstd,heistd]
                self.writein('BASIC'+get_date, col, value)
                self.writein('azi' + get_date, prn, azi)
                self.writein('ele' + get_date, prn, ele)
                self.writein('snr' + get_date, prn, snr)
                time = temp[0]
        print('Write complete! \n')

    def getcol(self,table):
        self.cursor.execute("select * from %s"%table)
        col_name_list = [tuple[0] for tuple in self.cursor.description]
        return col_name_list




    def close(self):
        self.db.close()
