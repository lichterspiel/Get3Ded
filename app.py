from flask import Flask, render_template, redirect, request, session
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
import helper
import sqlite3


app = Flask(__name__)
app.config["SECRET KEY"] = "dsd8+s97#*f89s#9ks"

#socketio init
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("start.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username").lower()
        password = request.form.get("password")
        if username == "":
            return "no username given"
        if password == "":
            return "no password given"

        with sqlite3.connect("test.db") as db:
            c = db.cursor()
            user =  helper.get_user(c, username, password)
            if user == None:
                return "wrong username"
            else:
                if check_password_hash(user[0], password):
                    session["username"] = username
                    return "logged in"
           

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username").lower()
        password = generate_password_hash(request.form.get("password"))
        # open db and add to it if username, pw is not empty and username does not already exist
        with sqlite3.connect("test.db") as db:
            c = db.cursor()
            if helper.register_user(c, username, password):
                db.commit()
                return redirect("/")
            else:
                return "error"

@app.route("/play", methods=["GET", "POST"])
def play():
    return render_template("play.html")

# chat event shit 
@socketio.on("my_event", namespace="/play")
def handle_my_custom_event(json):
    print(f"received {str(json)}")
    emit("my response", json)


if __name__ == "__main__":
    socketio.run(app, debug=True)
