from pymongo import MongoClient
from flask import Flask, jsonify, request
from flask_cors import cross_origin
# from utils import requires_auth

app = Flask(__name__)

mongo = MongoClient("mongodb://mongo:27017/patients")

app.url_map.strict_slashes = False


@app.route("/test/")
def test():
    return jsonify("online - response from admin-backend")


@app.route('/update_medical_history/<int:id>/', methods=['GET', 'POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
# @requires_auth
def update_medical_history(id):
    patients = mongo.db.patients
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        weight = request.form['weight']

        myquery = {"id": id}
        newvalues = {"$set": {"fname": fname, "lname": lname, "age": age, "weight": weight}}

        patients.update_one(myquery, newvalues)

        return "redirect"

    patient = patients.find_one({'id': id})
    return jsonify(
        {
            'id': patient['id'],
            'fname': patient['fname'],
            'lname': patient['lname'],
            'age': patient['age'],
            'weight': patient['weight'],
        }
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
