import sqlite3

from flask_restful import reqparse, Resource
from werkzeug.security import generate_password_hash

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field can not be blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field can not be blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "Username already existed!"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(
            query, (data['username'], generate_password_hash(data['password'])))

        connection.commit()
        connection.close()

        return {"message": "User created succefully"}, 201
