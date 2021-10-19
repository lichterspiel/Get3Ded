from flask import Flask, render_template, redirect, request, session, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from helper import *
import sqlite3

login_blueprint = Blueprint("login_blueprint", __name__, template_folder="templates")

DB = "test.db"

#================= ROUTES ====================#


@login_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@login_blueprint.route("/login", methods=["GET","POST"])
def login():
    # forget any user
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username").lower()
        password = request.form.get("password")
        if not username:
            return "no username given"
        if not password: 
            return "no password given"

        with sqlite3.connect(DB) as db:
            c = db.cursor()
            user =  get_user(c, username)
            if user == None:
                return "wrong username"
            else:
                if check_password_hash(user[0], password):
                    session["username"] = username
                    return redirect(url_for("index"))

@login_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username").lower()
        if request.form.get("check_password") != request.form.get("password"):
            return "passwords not identical"
        password = generate_password_hash(request.form.get("password"))
        # open db and add to it if username, pw is not empty and username does not already exist
        with sqlite3.connect("test.db") as db:
            c = db.cursor()
            if register_user(c, username, password):
                db.commit()
                return redirect("/")
            else:
                return "error"



