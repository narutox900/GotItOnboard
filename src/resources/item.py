from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field can not be blank!'
                        )
    parser.add_argument('store_id',
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
        new_item = ItemModel(None, name, data['price'], data['store_id'])
        try:
            new_item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'}, 401

        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if not item:
            return {'message': f'No item with name {name} exists'}, 400

        item.delete_from_db()

        return {'message': f'Item {name} deleted'}, 200

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(None, name, data['price'])

        if item:
            try:
                item.price = data['price']
                item.store_id = data['store_id']
            except:
                return {'message': 'An error occured updating the item'}

        else:
            try:
                item = ItemModel(None, name, data['price'], data['store_id'])
            except:
                return {'message': 'An error occured inserting the item'}

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        try:
            return ItemModel.get()
        except Exception as e:
            print(e)

