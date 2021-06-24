import os

from flask import Flask
from flask.json import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, UserLogin


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object('config.DevConfig')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from db import db
    db.init_app(app)

    api = Api(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    jwt = JWTManager(app)

    # @jwt.unauthorized_loader
    # @jwt.invalid_token_loader
    # @jwt.expired_token_loader
    # @jwt.user_lookup_error_loader
    def my_invalid_token_callback(jwt_header, jwt_payload):
        print(jwt_header)
        print(jwt_payload)
        return jsonify({'message': 'custom message go here'}), 401

    api.add_resource(UserLogin, '/auth')
    api.add_resource(Item, '/items/<int:_id>')
    api.add_resource(ItemList, '/items')
    api.add_resource(Store, '/stores/<int:_id>')
    api.add_resource(StoreList, '/stores')
    api.add_resource(UserRegister, '/register')

    return app
