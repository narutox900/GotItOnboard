import os

from flask import Flask, app
from flask_restful import Api
from flask_jwt import JWT

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import authenticate, identity

# if __name__ == '__main__':
#     app.run(port=5000, host='0.0.0.0', debug=True)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile('config.py')
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

    jwt = JWT(app, authenticate, identity)  # /auth
    api.add_resource(Item, '/items/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(Store, '/stores/<string:name>')
    api.add_resource(StoreList, '/stores')
    api.add_resource(UserRegister, '/register')

    return app
