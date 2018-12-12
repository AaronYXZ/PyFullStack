from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource): ## create Class Item that inherits Class Resource
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item ## no need to use jsonify in flask_restful
        return {"item": None}, 404
    ## what's the most popular http status code: 200

    def post(self, name):
        item = {"name":name, "price":15.00}
        items.append(item)
        return item, 201

api.add_resource(Item, '/item/<string:name>')



app.run(port=5001)



