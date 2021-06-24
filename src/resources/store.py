from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.store import StoreModel


class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This field can not be blank!'
                        )

    def get(self, _id):
        row = StoreModel.find_by_id(_id)

        if row:
            return row.json()

        return {'message': 'Store not found'}, 404

    @jwt_required()
    def delete(self, _id):
        store = StoreModel.find_by_id(_id)
        if not store:
            return {'message': f'No store with id {_id} exists'}, 400

        store.delete_from_db()

        return {'message': f'Store {_id} deleted'}, 200


class StoreList(Resource):
    def get(self):
        return StoreModel.get_all()

    @jwt_required()
    def post(self):
        data = Store.parser.parse_args()

        if StoreModel.find_by_name(data['name']):
            return {'message': f'A store with name: {data["name"]} already exists'}, 400

        new_item = StoreModel(data["name"])
        new_item.save_to_db()

        return new_item.json(), 201
