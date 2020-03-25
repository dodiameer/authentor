import eel
import sqlite3
import hashlib

def tableCheck():
   cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
   if cursor.fetchone():
      i = 1;
   else:
      cursor.execute("CREATE TABLE users(id integer PRIMARY KEY, username text, password text)")
      db.commit()

def hasher(password):
   hashed_password = hashlib.sha256(password.encode()).hexdigest()
   return hashed_password

eel.init('web') 
db = sqlite3.connect("users.db")
cursor = db.cursor()
tableCheck()

@eel.expose
def authenticate(username, password):
   encrypt = hasher(password)
   cursor.execute("SELECT 1 TOP FROM users WHERE username = ? AND password = ?", (username, encrypt))
   result = cursor.fetchone()
   if result:
      eel.receiver("true")
   else:
      eel.receiver("false")


@eel.expose
def register(usrn, pswd):
   encrypt = hasher(pswd)
   cursor.execute("SELECT 1 TOP FROM users WHERE username = ?", (usrn,))
   result = cursor.fetchone()
   if result:
      eel.receiver("false")
   else:
      cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (usrn, encrypt))
      db.commit()
      eel.receiver("true")


eel.start('main.html', size=(500, 450), mode='chrome')