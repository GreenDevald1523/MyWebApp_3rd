import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="123456",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            if username and password and records:
                return render_template('account.html', full_name=records[0][1], log=username, pas=password)
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if str(name) and str(login) and str(password):
            cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),))
            records = cursor.fetchall()
            if records:
                return redirect("/registration/")
            else:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))
                return redirect('/login/')

        conn.commit()

    return render_template('registration.html')
