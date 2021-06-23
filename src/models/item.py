import db


class ItemModel():
    def __init__(self, _id, name, price):
        self.id = _id
        self.name = name
        self.price = price

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        cursor = db.get_db()

        query = 'SELECT * FROM items WHERE name = ?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            return cls(*row)

        return None

    def insert(self):
        cursor = db.get_db()
        query = 'INSERT INTO items VALUES (NULL, ?, ?)'
        lastid = cursor.execute(query, (self.name, self.price)).lastrowid
        cursor.commit()
        return lastid

    def update(self):
        cursor = db.get_db()

        query = 'UPDATE items SET price = ? WHERE name = ?'
        cursor.execute(query, (self.price, self.name))
        cursor.commit()

    @classmethod
    def delete(cls, name):
        cursor = db.get_db()

        query = 'DELETE FROM items WHERE name = ?'
        cursor.execute(query, (name,))
        cursor.commit()

    @staticmethod
    def get():
        cursor = db.get_db()

        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        return result
