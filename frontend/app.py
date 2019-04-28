from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
import requests
from utils import get_header_for_auth, PatientForm, create_url_for_service, invoke_service

app = Flask(__name__)

app.url_map.strict_slashes = False


@app.route("/hello_world/")
def hello_world():
    response = invoke_service(service="backend", page_name="hello_world")
    return render_template('index.html', msg=response['message'])


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username'].lower()
        password = request.form['password']
        users = invoke_service(page_name="view_users", service="utils-backend")

        try:
            username = users[username]
            if username[password] != password:
                raise KeyError("Password was incorrect")
            role = username["role"]
        except KeyError:
            return render_template("login.html", msg="Incorrect username or password...")
        session['logged_in'] = True
        session["jwt_header"] = get_header_for_auth(role=role)
        return render_template("index.html", msg="You have been logged in...")
    return render_template("login.html")


@app.route("/logout/")
def logout():
    session.clear()
    return render_template("index.html", msg="You have been logged out...")


@app.route("/view_medical_history/<int:id>/")
def view_medical_history(id):
    patient = invoke_service(
        service="backend",
        page_name="view_medical_history",
        id=id,
        headers=session["jwt_header"]
    )

    return render_template(
        'view_medical_history.html', 
        id=patient['id'], 
        fname=patient['fname'],
        lname=patient['lname'], 
        age=patient['age'], 
        conditions=patient['conditions'],
        weight=patient['weight']
    )


@app.route('/update_medical_history/<int:id>/', methods=['GET', 'POST'])
def update_medical_history(id):
    patient = invoke_service(
        page_name="update_medical_history",
        id=id,
        service="admin-backend",
        headers=session["jwt_header"]
    )
    form = PatientForm(request.form)
    try:
        form.fname.data = patient['fname']
        form.lname.data = patient['lname']
        form.age.data = patient['age']
        form.weight.data = patient['weight']
    except TypeError:
        return patient
    if request.method == 'POST' and form.validate():

        admin_backend_url = create_url_for_service("update_medical_history", id, service="admin-backend")

        response = requests.post(admin_backend_url, data=request.form, headers=session["jwt_header"])

        if response.text == "redirect":
            flash('Patient updated', 'success')
            return redirect(url_for('view_patients'))
    return render_template('update_medical_history.html', form=form)


@app.route("/view_patients/", methods=['GET', 'POST'])
def view_patients():
    patients = invoke_service(
        service="backend",
        page_name="view_patients",
        headers=session["jwt_header"]
    )

    return render_template(
        'view_patients.html',
        patients=patients
    )


@app.route("/test/view_patients/", methods=['GET', 'POST'])
def test_view_patients_invalid_jwt():
    jwt = "1nv4l1DJwT"
    header = {
        'Authorization': "Bearer {token}".format(token=jwt)
    }
    patients = invoke_service(service="backend", page_name="view_patients", headers=header)
    return render_template(
        'view_patients.html',
        patients=patients
    )


@app.route("/test/invoke_service_header/", methods=['GET', 'POST'])
def test_headers():
    return jsonify(session["jwt_header"])


@app.route("/test/view_users/", methods=['GET'])
def test_view_users():
    users = invoke_service(page_name="view_users", service="utils-backend")
    return jsonify(users)


@app.route("/db/populate", methods=['GET'])
def populate_db():
    invoke_service(page_name="db/populate", service="utils-backend")
    return render_template("index.html", msg="DB has been populated.")


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True, host='0.0.0.0')
