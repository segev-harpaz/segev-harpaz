from flask import Flask, render_template, request
import psycopg2
from datetime import datetime
from database_connection import database_connection
app = Flask(__name__)
global database
database = database_connection()


@app.route('/')
def student():
    return render_template('projectHTML.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    global database
    if request.method == 'POST':
        result = request.form
        result1 = str(result)[:-2]
        num = result1.split(',')
        data = []
        for i in range(1, 6, 2):
            data.append(str(num[i][2:-2]))
        print(data)
        database.connect()
        if database.isin('project_database', data):
            database.close_db()
            return render_template('projectHTML.hmtl', result='change the name, password or id')
        else:
            database.close_db()
            return render_template('pass.html')


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
            data.append(num[i][2:-2])
        if data[0] == 'admin' and data[1] == 'admin123':
            database.connect()
            tab = database.table_column('time')
            print(tab)
            return render_template('admin.html', tab = tab)
        elif database.isin('project_database', data):
            database.connect()
            print(database.on_time(data))
            if database.on_time(data):
                database.close_db()
                return render_template('pass.html')
            else:
                return render_template('signin.html', aaa = 'your lesson is not now')
        else:
            return render_template('signinn.html', aaa = 'the password or name is incoreect')


@app.route('/sign_in2/show_table', methods=['POST', 'GET'])
def show_table():
    global database
    if request.method == 'POST':
        result = request.form
        result = str(result)[:-2]
        result = result.split(',')
        result = result[1][2:-2]
        database.connect()
        table = database.do(database.signin1(result))
        database.close_db()
        return render_template('show_table.html', table = table)


@app.route('/sign_in2/show_table/delete', methods = ['POST', 'GET'])
def delete():
    global database
    if request.method == 'POST':
        result = request.form
        result = str(result)[:-2]
        result = result.split(',')
        result = result[1][2:-2]
        database.connect()
        if database.isin('project_database', result):
            database.delete('project_database', result)
            database.delete(database.signin1(result), result)
            table = database.do(database.signin1(result))
            database.close_db()
            return render_template('show_table.html', table=table)
        else:
            table = database.do(database.signin1(result))
            database.close_db()
            return render_template('show_table.html', pro='this user is not exist', table=table)


@app.route('/sign_in2/create', methods=['POST', 'GET'])
def create():
    global database
    if request.method == 'POST':
        days = ['sunday', 'monday', 'tuesday', 'wensday', 'thursday', 'friday']
        option_data = ''
        for i in range(len(days)):
            if str(request.form.get(days[i])) != 'none':
                days[i] = i
                option_data += (str(request.form.get(days[i])).replace('-', ',').replace(':', '')) + ',' + days[i] + ','
            else:
                days.remove(days[i])
            counter += 1
        print(days)
        option_data = option_data[:-1]
        database.connect()
        table_name = request.form.get('asd')
        days.insert(0, 'name varchar(20), ')
        database.create(table_name, days)
        database.add_column('time', table_name + ' varchar(60), ')
        database.insert('time', table_name, option_data)
        database.close_db()
        return render_template('admin.html')


if __name__ == '__main__':
    app.run()
