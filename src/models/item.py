from os import name
import sqlite3

from flask import jsonify

import db


class ItemModel():
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        cursor = db.get_db()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            print("found something")
            return cls(*row)

        print("nothing found")
        return None

    def insert(self):
        cursor = db.get_db()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))
        cursor.commit()

    def update(self):
        cursor = db.get_db()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (self.price, self.name))
        cursor.commit()
