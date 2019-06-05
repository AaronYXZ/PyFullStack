from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
## every resource has to be a class

app = Flask(__name__)
api = Api(app)


items = []


class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {'item': None}, 404

    def post(self, name):
        item = {'name': name, 'price':12.00}
        items.append(item)
        return item

api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/student/Cris



app.run(port=5001)



## 404 not found
## 200 ok
## 201