from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from security import authenticate, identity
from resources.item import Item, ItemList
from resources.user import UserRegister

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) ## auth



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, "/register")

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    # app.run(debug=True)  # important to mention debug=True
    app.run(port = 5001)