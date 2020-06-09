import psycopg2
from datetime import datetime, date


class database_connection:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = psycopg2.connect(dbname='tftyiqbk', user='tftyiqbk', password='ioia30LFy_tPe-xsKDEfSalK-jlBC7j_',
                                host='kandula.db.elephantsql.com')
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def get_data(self, table_name):
        self.cursor.execute('select * from ' + table_name)
        return self.cursor.fetchall()

    def table_column(self, table_name):
        self.cursor.execute('select column_name from information_schema.columns where table_name = %s', (table_name,))
        ttt = self.cursor.fetchall()
        x = []
        for i in ttt:
            x.append(i[0])
        return x

    def do(self, table_name):
        table_data = self.get_data(table_name)
        column_name = self.table_column(table_name)
        table_data.insert(0, column_name)
        return table_data

    def isin(self, table_name, data):
        table_data = self.get_data(table_name)
        for row in table_data:
            for i in range(len(data)):
                if row[i] == data[i]:
                    return True
        return False

    def sign_in(self, data):
        table_data = self.get_data('project_database')
        for row in table_data:
            if data[0] == row[0] and data[1] == row[1]:
                return row[7][:-1]
        return ''

    def signin1(self, data):
        table_data = self.get_data('project_database')
        for row in table_data:
            if data == row[0]:
                return row[7][:-1]
        return ''

    def times(self, cla):
        self.cursor.execute('select ' + cla + ' from time')
        for row in  self.cursor.fetchall():
            if row[0] != None:
                return row[0]

    def on_time(self, data):
        cla = self.sign_in(data)
        if cla != '':
            time = self.times(cla)
            date = datetime.now()
            day_now = date.strftime("%A")
            time_now = str(int(date.strftime("%H%M")) + 300)
            time = time.split(',')
            for i in range(0, len(time), 3):
                if day_now.lower() == time[i + 2] and int(515) - 5 < int(time_now) < int(515) + 15:
                    return True
            return False

    def delete(self, table_name, name):
        sql = 'delete FROM ' + table_name + ' WHERE name = %s'
        self.cursor.execute(sql, (name,))
        self.conn.commit()

    def insert(self, table_name, columns, values):
        column_data = ''
        for row in columns:
            column_data += row + ', '
        column_data = column_data[:-2]
        sql = 'insert into ' + table_name + ' (' + column_data + ') values ('
        for row in range(len(columns)):
            sql += '%s, '
        sql = sql[:-2]
        sql += ')'
        print(sql)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def create(self, table_name, columns):
        column_data = columns[0]
        columns.remove(columns[0])
        today = str(date.today())[5:]
        today = today.split('-')
        for i in range(len(today)):
            today[i] = today[i].replace('0','')
        month = int(today[0])
        day = int(today[1])
        for i in range(7):
            if (columns[0] == (date.today().weekday()+ 2 + i) % 7):
                break
            else:
                day +=1
                if day > 31:
                    day=1
                    month += 1
        for i in range(30):
            if day < 10:
                column_data += 'a' + str(month) + '0' + str(day) + ' varchar(1), '
            else:
                column_data += 'a' + str(month) + str(day) + ' varchar(1), '
            day += int(columns[i % len(columns)])
            if day > 31:
                day -= 31
                month += 1
        column_data = column_data[:-2]
        sql = 'create table ' + table_name + ' (' + column_data + ')'
        self.cursor.execute(sql)
        self.conn.commit()

    def add_column(self, table_name, column_name):
        sql = 'alter table ' + table_name + ' add ' + column_name + ' varchar(60)'
        self.cursor.execute(sql)
        self.conn.commit()

    def update(self, table_name, column_name, values, checker):
        column_data = ''
        for i in range(len(column_name)):
            column_data += column_name[i] + ' = %s, '
            if len(column_name) - i == 2 and checker:
                column_data = column_data[:-2]
                column_data += ' WHERE '
        column_data = column_data[:-2]
        sql = 'UPDATE ' + table_name + ' SET ' + column_data
        self.cursor.execute(sql, values)
        self.conn.commit()

    def late(self, data):
        cla = self.sign_in(data)
        if cla != '':
            time = self.times(cla)
            date = datetime.now()
            day_now = date.strftime("%A")
            time_now = str(int(date.strftime("%H%M")) + 300)
            time = time.split(',')
            for i in range(0, len(time), 3):
                if day_now.lower() == time[i + 2] and int(time[i]) - 5 < int(time_now) < int(time[i]) + 2:
                    return True
            return False
