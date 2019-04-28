import os
from wtforms import Form, StringField, validators
import requests


class PatientForm(Form):
    fname = StringField('First Name', validators=[validators.Length(min=1, max=20)])
    lname = StringField('Last Name', validators=[validators.Length(min=1, max=20)])
    age = StringField('Age', validators=[validators.Length(min=1, max=3)])
    weight = StringField('Weight', validators=[validators.Length(min=1, max=4)])


# noinspection PyBroadException
def invoke_service(service, page_name, id="", headers=None):
    if headers is None:
        headers = {}
    url = create_url_for_service(page_name, id, service)
    try:
        res = requests.get(url, headers=headers)
    except Exception:
        return "Error with {url}.".format(url=url)
    try:
        response = res.json()
    except ValueError:
        try:
            return res
        except Exception:
            return "Response from {url} won't parse to json or return the response(if already json)".format(url=url)
    return response


def create_url_for_service(page_name, id="", service=""):
    services = {
        "admin-backend": {
            "host": "ADMIN-BACKEND-SERVICE-HOST",
            "port": "ADMIN-BACKEND-SERVICE-PORT",
        },
        "utils-backend": {
            "host": "UTILS-BACKEND-SERVICE-HOST",
            "port": "UTILS-BACKEND-SERVICE-PORT",
        },
        "backend": {
            "host": "BACKEND-SERVICE-HOST",
            "port": "BACKEND-SERVICE-PORT",
        },
        "frontend": {
            "host": "FRONTEND-SERVICE-HOST",
            "port": "FRONTEND-SERVICE-PORT",
        },
    }

    be_host = os.getenv('{host}'.format(host=services[service]["host"]), '{service}'.format(service=service))
    be_port = os.getenv('{port}'.format(port=services[service]["port"]), '5000')
    url = 'http://{host}:{port}/{page_name}/{id}'.format(host=be_host, port=be_port, page_name=page_name, id=id)
    return url


def get_header_for_auth(role=None):
    header = dict()

    response = invoke_service(service="utils-backend", page_name="api/generate_token/{role}".format(role=role))

    # noinspection PyTypeChecker
    header['Authorization'] = "Bearer {token}".format(token=response["access_token"])

    return header
