from flask import Flask, render_template, request
from database_connection import database_connection
from datetime import datetime
app = Flask(__name__)
global database
database = database_connection()


@app.route('/')
def student():
    global database
    try:
        database.connect()
        tab = database.table_column('time')
        database.close_db()
        return render_template('projectHTML.html', tab = tab)
    except:
        return render_template('problem.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    global database
    if request.method == 'POST':
        if request.form.get('times') == None:
            return render_template('projectHTML.html', result='please create class')
        result = request.form
        result1 = str(result)[:-2]
        num = result1.split(',')
        data = []
        for i in range(1, 6, 2):
            if str(num[i][2:-2]) == '':
                return render_template('projectHTML.html', result='you must fill the form')
            data.append(str(num[i][2:-2]))
        try:
            database.connect()
            if database.isin('project_database', data):
                tab = database.table_column('time')
                database.close_db()
                return render_template('projectHTML.html', result='change the name, password or id', tab = tab)
            else:
                database.close_db()
                return render_template('pass.html', result = request.form.get('times'))
        except:
            return render_template('problem.html')


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        return render_template('signin.html')


@app.route('/sign_in2', methods=['POST', 'GET'])
def sign_in2():
    global database
    if request.method == 'POST':
        result = request.form
        result1 = str(result)[:-2]
        num = result1.split(',')
        data = []
        for i in range(1, 4, 2):
            if num[i][2:-2] == '':
                return render_template('signin.html', aaa='you must fill the form')
            data.append(num[i][2:-2])

        database.connect()
        if data[0] == 'admin' and data[1] == 'admin123':
            tab = database.table_column('time')
            database.close_db()
            return render_template('admin.html', tab = tab)
        elif database.isin('project_database', data):
            if database.on_time(data):
                database.update('project_database', ( 'connected_time', 'connected_signin', 'on_time','name'), ( database.on_time(data), True, database.late(data),data[0]),True)
                database.close_db()
                return render_template('pass.html')
            else:
                database.close_db()
                return render_template('signin.html', aaa = "your lesson is not now")
        else:
            return render_template('signinn.html', aaa = 'the password or name is incoreect')


@app.route('/sign_in2/show_table', methods=['POST', 'GET'])
def show_table():
    global database
    if request.method == 'POST':
        database.connect()
        result = request.form.get('class_name')
        table = database.do(result)
        database.close_db()
        return render_template('show_table.html', table = table, result = '')


@app.route('/sign_in2/create', methods=['POST', 'GET'])
def create():
    global database
    if request.method == 'POST':
        days = ['sunday', 'monday', 'tuesday', 'wensday', 'thursday', 'friday']
        option_data = ''
        for i in range(len(days)):
            print(days[i])
            if str(request.form.get(days[i])) != 'none':
                option_data += str(request.form.get(days[i])).replace('-', ',').replace(':', '') + ',' + days[i] + ','
                days[i] = i + 1
            else:
                days[i] = ''
        days = list(dict.fromkeys(days))
        try:
            days.remove('')
        finally:
            for i in range(len(days) -1, 0, -1):
                days[i] = days[i] - days[i-1]
            option_data = option_data[:-1]
            database.connect()
            table_name = request.form.get('asd')
            if database.isin('time', [table_name]):
                return render_template('admin.html', dudu = 'this class is exist')
            days.insert(0, 'name varchar(20), ')
            database.create(table_name.replace(' ', '_'), days)
            database.add_column('time', table_name.replace(' ', '_'))
            database.insert('time', [table_name.replace(' ', '_')], [option_data])
            tab = database.table_column('time')
            database.close_db()
            return render_template('admin.html', tab = tab)


if __name__ == '__main__':
    app.run()
