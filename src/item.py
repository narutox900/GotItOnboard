import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field can not be blank!"
                        )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 201

        return None

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    def get(self, name):
        row = Item.find_by_name(name)

        if row:
            return row

        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):

        if Item.find_by_name(name):
            return {'message': f"An item with name '{name} already exists"}, 400

        data = Item.parser.parse_args()
        new_item = {'name': name, 'price': data['price']}
        self.insert(new_item)

        return new_item, 201

    @jwt_required()
    def delete(self, name):
        if not Item.find_by_name(name):
            return {'message': f"No item with name {name} exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': f"Item {name} deleted"}, 200

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        if Item.find_by_name(name):
            try:
                self.update(item)
            except:
                return {'message': 'An error occured updating the item'}

        else:
            try:
                self.insert(item)
            except:
                return {'message': 'An error occured inserting the item'}

        return item


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}
