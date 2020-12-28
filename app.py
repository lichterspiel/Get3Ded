from flask import Flask, render_template, redirect, request, session, url_for
from flask_socketio import SocketIO, emit, join_room, send
from werkzeug.security import generate_password_hash, check_password_hash
import helper
from helper import login_required
from ttt_logic import *
import sqlite3
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
#app.config["SECRET_KEY"] = "!§)(§HOIAq38h143ui214h1)"

# sessions
app.config["SESSION_PERMANENT"] = False
#socketio init
socketio = SocketIO(app)

# board
board = [[0 for i in range(3)]for i in range(3)]

@app.route("/")
def index():
    return render_template("start.html")


@app.route("/login", methods=["GET","POST"])
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

        with sqlite3.connect("test.db") as db:
            c = db.cursor()
            user =  helper.get_user(c, username, password)
            if user == None:
                return "wrong username"
            else:
                if check_password_hash(user[0], password):
                    session["username"] = username
                    return redirect(url_for("index"))
           

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

@app.route("/create", methods=["GET", "POST"])
def create_room():
    if request.method == "GET":
        return render_template("create_room.html")
    else:
        if not  request.form.get("room"):
            return("No room given")
        else:
            session["j_room"] = request.form.get("room")
            return(redirect(url_for("play")))

@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    return render_template("play.html", room = session.get("j_room"), username = session.get("username"))

# chat event shit 
@socketio.on("my_event") 
def handle_my_custom_event(json):
    print(f"received {str(json)}")
    emit("my response", json)

@socketio.on('join', namespace="/play")
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(username+ "connected " + room)
    send(username + ' has entered the room.', room=room)

@socketio.on("move", namespace="/play")
def move(data):
    # extract y and x coordinates from json
    y = int(data["id"][0])
    x = int(data["id"][1])

    #check if at coordinates is valid
    if board[y][x] == 0:
        board[y][x] = "X"
        emit("valid", data)
    else:
        emit("invalid")

    








if __name__ == "__main__":
    socketio.run(app, debug=True)
