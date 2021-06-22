import sqlite3
from sqlite3.dbapi2 import connect

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE if not exists users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'tung', '1234')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'tung2', '1234'),
    (3, 'tung3', '1234')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
