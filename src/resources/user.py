from flask_restful import reqparse, Resource

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

        user = UserModel(None, data['username'], data['password'])
        user.register()

        return {'message': 'User created succefully'}, 201
