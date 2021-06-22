import sqlite3
import db


class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        cursor = db.get_db()

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = UserModel(*row)
        else:
            user = None

        return user

    @classmethod
    def find_by_id(cls, _id):
        cursor = db.get_db()

        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = UserModel(*row)
        else:
            user = None

        return user
