import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

from db import db


app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose123'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # allows us to call /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

db.init_app(app)


@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify(
        {'message': 'Could not authorize. Did you include a valid Authorization header?'}), 401


if __name__ == '__main__':
    if app.config['DEBUG']:
        with app.app_context():
            def create_tables():
                db.create_all()
            create_tables()

    app.run(port=5000)
