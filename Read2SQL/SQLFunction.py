import pymysql

def sixty2ten(data_input):
    for i in range(len(data_input)):
        Ndeg=data_input[0:(data_input.rfind(".")-2)]
        Nmin=data_input[(data_input.rfind(".")-2):-1]
        N=float(Ndeg)+float(Nmin)/60
    return N

def str2float(string):
    if not string:
        return -1.0
    if string:
        return float(string)

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
        sql = 'select %s from %s where id = %d' %(column, table, index)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()[0]
            return result
        except:
            print('Error: unable to fetch data')

    def readall(self, column, table, type = str):
        sql = 'select %s from %s' %(column, table)
        try:
            self.cursor.execute(sql)
            """convert 2D tuple to 1D list"""
            """ (('20',),('None',)) -->  ['20',None]  """
            result = [element[0] for element in self.cursor.fetchall()]
            return result
        except:
            print('Error: unable to fetch data')

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
            self.cursor.execute("DROP TABLE IF EXISTS %s" %table)
            self.cursor.execute(sql)
            print('Success: you have replace the table of %s' %table)
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
        self.cursor.execute(sql)
        try:
            self.db.commit()
        except:
            self.db.rollback()

    def nmea2sql(self,file_path:str,get_date:str):
        with open(file_path, encoding='utf-8') as f_in:
            line = f_in.readline()
            temp = line.strip().split(',')
            time = temp[0]
            while line:
                while time == temp[0]:
                    if 'RMC' in temp[1] and temp[3] == 'A':
                        lon = sixty2ten(temp[6])
                        lat = sixty2ten(temp[4])
                        speed = str2float(temp[8])
                        course = str2float(temp[9])
                        date = temp[10]
                        time = temp[0]
                    elif 'GGA' in temp[1] and temp[2] != '':
                        SU = int(temp[8])
                        HDOP = str2float(temp[9])
                        height = float(temp[10])
                    line = f_in.readline()
                    temp = line.strip().split(',')
                col = ['Time','Date','Lon','Lat','Speed','Course','SU','HDOP','Height']
                value = [time,date,lon,lat,speed,course,SU,HDOP,height]
                self.writein('BASIC'+get_date,col,value)
        print('Write complete! \n')





    def close(self):
        self.db.close()
