from scapy.all import *
from threading import Thread, Timer
from datetime import timedelta, date
from database_connection import database_connection
global database
database = database_connection()


def http_header(packet):
    http_packet = str(packet)
    if 'segevharpaz1.pythonanywhere.com' in http_packet and 'times' in http_packet:
        print('yes')
        return GET_print(packet)


def GET_print(packet1):
    global database
    ret = "\n".join(packet1.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
    stack = ret.split('\n')
    data = stack[15].split('&')
    x = []
    columns = []
    for i in range(5):
        x.append(data[i].split('=')[1])
        columns.append(data[i].split('=')[0])
    del x[3]
    del columns[3]
    print(x[3])
    database.connect()
    x.insert(3, str(packet1[0][Ether].src))
    columns.insert(3, 'mac')
    print(not(database.isin('project_database', x)))
    if not(database.isin('project_database', x)):
        a = ['connected_wifi', 'connected_time', 'connected_signin','on_time']
        columns = columns + a
        b = [True,True,True,True]
        x = x + b
        database.insert('project_database', columns, x)
        database.insert(x[4][:-1], ['name'], [x[0]])
    database.close_db()


def sniff1():
    global database
    while True:
        packets = sniff(count=1, filter='udp and (port 67 or 68) and ether src b8:27:eb:8a:0a:c9', iface='wlan0')
        database.connect()
        table_data = database.get_data('project_database')
        for row in table_data:
            if row[3] == packets[0][Ether].dst:
                print(2)
                column_name = ['connected_wifi', 'mac']
                values = [True, packets[0][Ether].dst]
                database.update('project_database', column_name, values, True)
        database.close_db()


def sniff2():
    while True:
        print(1)
        sniff(count=1, lfilter=http_header, filter='tcp port 80', iface='wlan0')


def dudu(q):
    global database
    print('chage true')
    if not q:
        print('end change')
        return create_q()
    database.connect()
    column = ['connected_wifi', 'connected_signin', 'connected_time', 'on_time']
    values = (False, False, False, False)
    database.update('project_database', column, values, False)
    data = q.pop(0)
    database.close_db()
    Timer(data, dudu, [q]).start()


def arrive_late(q):
    global database
    print('change data')
    if not q:
        print('end data')
        return create_q()
    database.connect()
    table_data = database.get_data('project_database')
    table_data1 = database.get_data('project_database')
    today = date.today()
    for row in table_data:
        for i in database.table_column(row[7][:-1]):
            if ('a' + str(today)[6:].replace('-', '') == i):
                if bool(row[4]) & bool(row[5]) and bool(row[6]):
                    if bool(row[8]):
                        columns = ['a' + str(today)[6:].replace('-', ''), 'name']
                        values = (0, row[0])
                        database.update(row[7][:-1], columns, values, True)
                    else:
                        columns = ['a' + str(today)[6:].replace('-', ''), 'name']
                        values = (1, row[0])
                        database.update(row[7][:-1], columns, values, True)
                else:
                    columns = ['a' + str(today)[6:].replace('-', ''), 'name']
                    values = (2, row[0])
                    database.update(row[7][:-1], columns, values, True)
    print(q)
    data = q.pop(0)
    print(data)
    database.close_db()
    Timer(data, arrive_late, [q]).start()


def create_q():
    q = [timedelta(seconds=180).total_seconds(), timedelta(seconds=180).total_seconds(),
         timedelta(seconds=180).total_seconds(),timedelta(seconds=180).total_seconds(), timedelta(seconds=180).total_seconds(),
         timedelta(seconds=180).total_seconds()]
    now = datetime.now().strftime('%H:%M:%S')
    now = datetime.strptime(now, '%H:%M:%S')
    reset_connection = datetime.strptime('5:23:00', "%H:%M:%S")
    late_check = datetime.strptime('05:22:00', "%H:%M:%S")
    delay = (reset_connection - now).total_seconds()
    delay1 = (late_check - now).total_seconds()
    if delay < 0:
        delay += timedelta(hours=24).total_seconds()
    if delay1 < 0:
        delay1 += timedelta(hours=24).total_seconds()
    Timer(delay, dudu, [q]).start()
    Timer(delay1, arrive_late, [q]).start()


def main():
    t = Thread(target=sniff1)
    t.start()
    s = Thread(target=sniff2)
    s.start()
    create_q()


if __name__ == '__main__':
    main()
