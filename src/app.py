import os

from flask import Flask, app
from flask_restful import Api
from flask_jwt import JWT

from resources.item import Item, ItemList
from resources.user import UserRegister
from security import authenticate, identity

# if __name__ == '__main__':
#     app.run(port=5000, host='0.0.0.0', debug=True)

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    import db
    db.init_app(app)

    api = Api(app)

    jwt = JWT(app, authenticate, identity)  # /auth
    api.add_resource(Item, '/items/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(UserRegister, '/register')

    return app
