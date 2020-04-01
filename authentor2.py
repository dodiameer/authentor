from flask import Flask, render_template, request, url_for, redirect
from flaskwebgui import FlaskUI
import sqlite3
import hashlib
import os
import sys

app = Flask(__name__)
DATABASE = 'static/db/authentor2.db'
ui = FlaskUI(app)

def tableCheck():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='users'")
    result = cursor.fetchone()
    if result:
        pass
    else:
        cursor.execute("CREATE TABLE users (id integer PRIMARY_KEY, username text, password text)")
        db.commit()
        cursor.execute("INSERT INTO users (username, password) VALUES ('admin', ?)", (encrypt('admin'),))
        db.commit()
        db.close()

def encrypt(password):
   hashed_password = hashlib.sha256(password.encode()).hexdigest()
   return hashed_password

def authenticate(username, password):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? and password=?", (username, encrypt(password)))
    result = cursor.fetchone()
    if result:
        db.close()
        return 'OK'
    else:
        db.close()
        return 'NOT FOUND'

def register(username, password):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    if username == "" or password == "":
        return 'ERR'
    else:
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        if result:
            db.close()
            return "ERR"
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, encrypt(password)))
            db.commit()
            db.close()
            return "DONE"


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        userIn = request.form['username']
        passIn = request.form['password']
        result = authenticate(userIn, passIn)
        if result == 'OK':
            return render_template('index.html', auth=True)
        elif result == 'NOT FOUND':
            return render_template('index.html', auth=False)
    else:
        return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def newAccount():
    if request.method == 'POST':
        userIn = request.form['username']
        passIn = request.form['password']
        result = register(userIn, passIn)
        if result == 'DONE':
            return redirect(url_for('index', auth='REG'))
        elif result == 'ERR':
            return render_template('register.html', registered=False)
    else:
        return render_template('register.html')

def mainApp():
    tableCheck()
    ui.run()