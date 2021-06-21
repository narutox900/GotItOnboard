import sqlite3
from sqlite3.dbapi2 import connect

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE if not exists users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE if not exists items (name text PRIMARY KEY, price real)"
cursor.execute(create_table)

connection.commit()

connection.close()
