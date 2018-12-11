from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
## every resource has to be a class

app = Flask(__name__)
api = Api(app)


items = []


class Student(Resource):
    def get(self, name):
        return jsonify({"student": name})

api.add_resource(Student, '/student/<string:name>') # http://127.0.0.1:5000/student/Cris



app.run(port=5001)



