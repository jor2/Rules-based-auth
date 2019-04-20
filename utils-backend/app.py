from flask import Flask, jsonify
import json
import http.client
from bson import json_util
from pymongo import MongoClient

app = Flask(__name__)

mongo = MongoClient("mongodb://mongo:27017/patients")

app.url_map.strict_slashes = False


@app.route("/api/generate_token/admin")
def generate_token_admin():
    data = get_auth0_api_data(role="admin")
    return data


@app.route("/api/generate_token/consultant")
def generate_token_consultant():
    data = get_auth0_api_data(role="consultant")
    return data


@app.route("/api/generate_token/doctor")
def generate_token_doctor():
    data = get_auth0_api_data(role="doctor")
    return data


@app.route("/api/generate_token/patient")
def generate_token_patient():
    data = get_auth0_api_data(role="patient")
    return data


def get_auth0_api_data(role):
    conn = http.client.HTTPSConnection("jor2.eu.auth0.com")
    payload = get_payload_for_user_role(role)
    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    data = json.loads(data)
    return jsonify(data)


def get_payload_for_user_role(role):
    payloads = {
        "admin": "{\"client_id\":\"Tlvh98YxZG6jqi6dUrXe7dHz5pg1bhtu\",\"client_secret\":\"YbqUFILFTecLcL9FvryjVLF5y2RRQb2pkRuDD368t6sqrvmIIB2ZLKclhAdmYKDu\",\"audience\":\"https://rba.com/admin\",\"grant_type\":\"client_credentials\",\"grant_id\":\"cgr_mlg8jdFbtXRH9LHP\"}",
        "consultant": "{\"client_id\":\"aFmOOGK2X7W8G7bFBXinyScuTL9Om6Ng\",\"client_secret\":\"QDXrL3mcfNd2Gom3w5qcBxn3B6be8h9J4yW6Hb9M8LqPxTivD7I8QusUjC2asKi0\",\"audience\":\"https://rba.com/consultant\",\"grant_type\":\"client_credentials\",\"grant_id\":\"cgr_bNEC65aPPa4Kpc3o\"}",
        "doctor": "{\"client_id\":\"3XFBbjTL6tsL9wH6iZQtkz3rKgGeiLwh\",\"client_secret\":\"bsgVPmP4XE4OFLysp35qPD5w0Mg-J1SZkmkbEFrAmAVhwAyUDliN573oQY82fQ-R\",\"audience\":\"https://rba.com/doctor\",\"grant_type\":\"client_credentials\",\"grant_id\":\"cgr_dwYUL53i3o8S2RyC\"}",
        "patient": "{\"client_id\":\"qkCsDTI4XkkpzdWS3PgIWPZaSEaAcgwJ\",\"client_secret\":\"XWcXK3izPliPn18PWScxiPM6AdmohQsB5_pBeUQrELJQZRhqhkw7Qrgh5ePrqs-0\",\"audience\":\"https://rba.com/patient\",\"grant_type\":\"client_credentials\",\"grant_id\":\"cgr_CJ7yzA6yQbY2D0U5\"}",
    }
    return payloads[role]


@app.route('/db/populate/patients')
def patients_populate_db():
    patient = mongo.db.patients
    patient.insert(
        {
            'id': 1,
            'fname': 'Jill',
            'lname': 'Smith',
            'age': '50',
            'weight': '63.3',
            'conditions': ['Stage 2 Diabetes', 'Cancer', 'Aids']
        }
    )

    patient.insert(
        {'id': 2,
         'fname': 'John',
         'lname': 'Smith',
         'age': '52',
         'weight': '86.2',
         'conditions': ['Heart Disease', 'Cancer']
         }
    )

    patient.insert(
        {
            'id': 3,
            'fname': 'Ryan',
            'lname': 'Gosling',
            'age': '25',
            'weight': '75',
            'conditions': ['Flu']
        }
    )

    patient.insert(
        {
            'id': 4,
            'fname': 'Sean',
            'lname': 'Winnot',
            'age': '21',
            'weight': '82',
            'conditions': ['Lupis']
        }
    )
    return "Patients Added."


@app.route('/db/populate/users')
def users_populate_db():
    users = mongo.db.users

    users.insert(
        {
            'id': 1,
            'username': 'admin',
            'password': 'password',
            'role': 'admin',
        }
    )
    users.insert(
        {
            'id': 2,
            'username': 'consultant',
            'password': 'password',
            'role': 'consultant',
        }
    )
    users.insert(
        {
            'id': 3,
            'username': 'doctor',
            'password': 'password',
            'role': 'doctor',
        }
    )
    users.insert(
        {
            'id': 4,
            'username': 'patient',
            'password': 'password',
            'role': 'patient',
        }
    )
    return "Users Added."


@app.route("/db/populate")
def populate_db():
    patients_populate_db()
    users_populate_db()
    return "db populated"


@app.route("/view_users", methods=['GET', 'POST'])
def view_users():
    users = mongo.db.users
    cursor = users.find()
    users = dict()
    for c in cursor:
        users[c["username"]] = {
            "password": c["password"],
            "role": c["role"]
        }
    if users is None:
        return jsonify("Cannot find any users")
    return json.dumps(users, default=json_util.default)


@app.route("/test/")
def test():
    return jsonify("online - response from utils-backend")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
