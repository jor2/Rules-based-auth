from bson import json_util
from pymongo import MongoClient
from flask import Flask, jsonify
import json
from flask_cors import cross_origin
# from utils import requires_auth

app = Flask(__name__)

mongo = MongoClient("mongodb://mongo:27017/patients")

app.url_map.strict_slashes = False


@app.route("/view_medical_history/<int:id>/")
@cross_origin(headers=['Content-Type', 'Authorization'])
# @requires_auth
def view_medical_history(id):
    patients = mongo.db.patients
    patient = patients.find_one({'id': id})
    return jsonify(
        {
            'id': patient['id'],
            'fname': patient['fname'],
            'lname': patient['lname'],
            'age': patient['age'],
            'conditions': patient['conditions'],
            'weight': patient['weight'],
        }
    )


@app.route("/view_patients", methods=['GET', 'POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
# @requires_auth
def view_patients():
    patients = mongo.db.patients
    cursor = patients.find()
    patients = list()
    for c in cursor:
        patients.append(c)
    return json.dumps(patients, default=json_util.default)


@app.route('/hello_world')
@cross_origin(headers=['Content-Type', 'Authorization'])
def hello_world():
    return jsonify(
        {
            'message': 'Hello World v1 - IBM Demo'
        }
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
