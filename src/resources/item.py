from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field can not be blank!'
                        )

    def get(self, name):
        row = ItemModel.find_by_name(name)

        if row:
            return row.json()

        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': f'An item with name: {name} already exists'}, 400

        data = Item.parser.parse_args()
        new_item = ItemModel(None, name, data['price'])
        try:
            new_item.id = new_item.insert()
        except:
            return {'message': 'An error occured inserting the item'}, 401

        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        if not ItemModel.find_by_name(name):
            return {'message': f'No item with name {name} exists'}, 400

        ItemModel.delete(name)

        return {'message': f'Item {name} deleted'}, 200

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(None, name, data['price'])

        if item:
            try:
                updated_item.id = item.id
                updated_item.update()
            except:
                return {'message': 'An error occured updating the item'}

        else:
            try:
                updated_item.id = updated_item.insert()
            except:
                return {'message': 'An error occured inserting the item'}

        return updated_item.json()


class ItemList(Resource):
    def get(self):
        result = ItemModel.get()

        items = []
        for row in result:
            items.append({'id': row[0], 'name': row[1], 'price': row[2]})

        return {'items': items}
