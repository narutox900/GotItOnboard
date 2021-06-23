from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        row = StoreModel.find_by_name(name)

        if row:
            return row.json()

        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'A store with name: {name} already exists'}, 400

        new_item = StoreModel(name)
        try:
            new_item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item'}, 500

        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {'message': f'No store with name {name} exists'}, 400

        store.delete_from_db()

        return {'message': f'Store {name} deleted'}, 200

class StoreList(Resource):
    @staticmethod
    def get():
        # return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}