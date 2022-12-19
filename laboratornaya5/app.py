import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(
    database="service_db",
    user="postgres",
    password="poly2212",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method =="POST":
        if request.form.get("login"):
            username = request.form.get("username")
            password = request.form.get("password")
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = cursor.fetchall()
            if len(records) == 1:
                _, full_name, login, password = records[0]
                return render_template("account.html", full_name=full_name, login=login, password=password)
            return render_template("login_error.html")

        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template("login.html")

@app.route("/registration/", methods=["POST", "GET"])
def registration():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            login = request.form.get("login")
            password = request.form.get("password")
            cursor.execute("INSERT INTO service.users(full_name, login, password) VALUES(%s, %s, %s);", (str(name), str(login), str(password)))
            conn.commit()
            return redirect("/login/")
        except Exception:
            return render_template("r_error.html")

    return render_template("registration.html")
