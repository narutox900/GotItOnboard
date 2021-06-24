from flask import jsonify
from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field can not be blank!'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field can not be blank!'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'Username already existed!'}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {'message': 'User created succefully'}, 201


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field can not be blank!'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field can not be blank!'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user and check_password_hash(user.password, data['password']):
            print(user.password)
            print(data)
            access_token = create_access_token(identity=user.id)
            return jsonify({"access_token": access_token, "user_id": user.id})
