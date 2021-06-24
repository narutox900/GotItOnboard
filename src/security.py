from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from werkzeug.security import check_password_hash

from models.user import UserModel

class Security(Resource):
    def post(self, username, password):
        user = UserModel.find_by_username(username)
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return jsonify({ "token": access_token, "user_id": user.id })
            


    def identity(payload):
        user_id = payload['identity']
        return UserModel.find_by_id(user_id)
