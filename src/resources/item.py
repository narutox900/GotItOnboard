from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This field can not be blank!'
                        )
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

    def get(self, _id):
        rows = ItemModel.find_by_id(_id)

        if rows:
            # return {'items': [row.json()] for row in rows}
            return rows.json()

        return {'message': 'Item not found'}, 404

    @jwt_required()
    def delete(self, _id):
        item = ItemModel.find_by_id(_id)
        if not item:
            return {'message': f'No item with id {_id} exists'}, 400

        item.delete_from_db()

        return {'message': f'Item {_id} deleted'}, 200

    @jwt_required()
    def put(self, _id):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_id(_id)

        if item:
            item.name = data['name']
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(None, data['name'],
                             data['price'], data['store_id'])

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return ItemModel.get_all()

    @jwt_required()
    def post(self):

        data = Item.parser.parse_args()

        if ItemModel.find_by_name(data['name']):
            return {'message': f'An item with name: {data["name"]} already exists'}, 400

        new_item = ItemModel(
            None, data['name'], data['price'], data['store_id'])
        try:
            new_item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'}, 401

        return new_item.json(), 201
