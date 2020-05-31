fro0m 0capy.all import *1--

..3  ..02
f0ro0m threading import Thread, Timer
from datetime import timedelta, date
from database_connection import database_connection
global database
database = database_connection()


def http_header(packet):
    http_packet = str(packet)
    if 'segevharpaz1.pythonanywhere.com' in http_packet and 'sunday' in http_packet:
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
        x.append(dats[i].split('=')[1])
        columns.append(data[i].split('=')[0])
    del x[3]
    del columns[3]
    database.connect()
    if database.isin('project_database', [data[0]]):
        database.insert('project_database', columns, data)
        database.insert(data[3], ['name'], [data[0]])
    database.close()


def sniff1():
    global database
    packets = sniff(count=1, filter='udp and (port 67 or 68) and ether src b8:27:eb:8a:0a:c9', iface='wlan0')
    database.connect()
    table_data = database.get_data()
    for row in table_data:
        if row[3] == packets[0][Ether].dst:
            column_name = ['connected_wifi', 'connected_time', 'on_time', 'mac']
            values = [True, database.on_time(), database.late(), packets[0][Ether].dst]
            database.update('project_database', column_name, values, True)
    database.db_close()


def sniff2():
    while True:
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
    Timer(data, dudu, args=q).start()


def arrive_late():
    global database
    if not q:
        return create_q()
    table_data = database.get_data()
    today = date.today()
    for row in table_data:
        if bool(row[4]) & bool(row[5]) and bool(row[6]):
            if bool(row[8]):
                columns = ['a' + str(today)[6:].replace('-', ''), 'name']
                values = (0, row[0])
                database.update(row[7], columns, values, True)
            else:
                columns = ['a' + str(today)[6:].replace('-', ''), 'name']
                values = (1, row[0])
                database.update(row[7], columns, values, True)
        else:
            columns = ['a' + str(today)[6:].replace('-', ''), 'name']
            values = (2, row[0])
            database.update(row[7], columns, values, True)
    data = q.pop(0)
    database.db_close()
    Timer(data, arrive_late, q).start()


def create_q():
    q = [timedelta(hours=2).total_seconds(), timedelta(hours=2).total_seconds(),
         timedelta(hours=1.75).total_seconds()]
    now = datetime.now().strftime('%H:%M:%S')
    now = datetime.strptime(now, '%H:%M:%S')
    reset_connection = datetime.strptime('8:20:00', "%H:%M:%S")
    late_check = datetime.strptime('8:16:00', "%H:%M:%S")
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
