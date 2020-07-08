from flask import Flask, request, render_template, session, url_for, logging, redirect, flash
from pymongo import MongoClient
import json
app = Flask(__name__)
client = MongoClient()
db = client['customer']
collec = db['xyz']


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        #print(json.dumps(request.form, indent=4))
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm password")
        if password == confirm:
            secure_password = str(password)
            entry = {'name': name,
                    'username': username,
                   'password': secure_password}
            existing_user = collec.find_one({'username': username})
            if existing_user is None:
                collec.insert(entry)
                flash("Registration successful", "success")
                return render_template("home.html")
            else:
                flash("Username already exist", "danger")
                return render_template("register.html")
        else:
            flash("Password does not match", "danger")
            return render_template("register.html")
    else:
        return render_template("register.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        data = collec.find_one(({'username': username, "password": password}))
        session['log'] = True
        if data:
            flash("You are logged in", "success")
            return render_template("home.html")
        else:
            flash("You are not registered", "danger")
            return render_template("register.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear
    flash("You are now logged out","success")
    return render_template("login.html")

app.secret_key="12ddededd"
app.run(debug=True)
