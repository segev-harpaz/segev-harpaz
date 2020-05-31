from scapy.all import *
from threading import Thread, Timer
from datetime import timedelta, date
from database_connection import database_connection
global database
database = database_connection()


def http_header(packet):
    http_packet = str(packet)
    if 'segevharpaz1.pythonanywhere.com' in http_packet and 'times' in http_packet:
        print('nigga')
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
    database.connect()
    x.append(str(packet1[0][Ether].src))
    columns.append('mac')
    print(x)
    if not(database.isin('project_database', x)):
        a = ['connected_wifi', 'connected_time', 'connected_signin','on_time']
        columns = columns + a
        b = [True,True,True,True]
        x = x + b
        print(x)
        print('x')
        database.insert('project_database', columns, x)
        print(x[3])
        print(x[0])
        database.insert(x[3][:-1], ['name'], [x[0]])
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
                column_name = ['connected_wifi', 'connected_time', 'on_time', 'mac']
                values = [True, database.on_time(row[0]), database.late(row[0]), packets[0][Ether].dst]
                database.update('project_database', column_name, values, True)
        database.close_db()


def sniff2():
    while True:
        print(1)
        sniff(count=1, lfilter=http_header, filter='tcp port 80', iface='wlan0')


def dudu(q):
    global database
    if not q:
        return create_q()
    database.connect()
    column = ['connected_wifi', 'connected_signin, connected_time']
    values = (False, False, False)
    database.update('project_database', column, values, False)
    data = q.pop(0)
    database.close_db()
    Timer(data, dudu, args=q).start()


def arrive_late(q):
    global database
    if not q:
        return create_q()
    database.connect()
    table_data = database.get_data('project_database')
    today = date.today()
    for row in table_data:
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
    data = q.pop(0)
    database.close_db()
    Timer(data, arrive_late, q).start()


def create_q():
    q = [timedelta(hours=2).total_seconds(), timedelta(hours=2).total_seconds(),
         timedelta(hours=1.75).total_seconds()]
    now = datetime.now().strftime('%H:%M:%S')
    now = datetime.strptime(now, '%H:%M:%S')
    reset_connection = datetime.strptime('23:45:00', "%H:%M:%S")
    late_check = datetime.strptime('00:44:00', "%H:%M:%S")
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