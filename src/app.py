from flask import Flask, app, request
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'key'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = []

class Item(Resource):
    # @app.route('/student/<string:name>')
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)

        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f"An item with name '{name} already exists"}, 400

        data = request.get_json()
        new_item = {'name': name, 'price': data['price']}
        items.append(new_item)
        return new_item, 201


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


app.run(port=5000, host='0.0.0.0', debug=True)
