from flask import Flask, render_template, redirect, request, session, url_for
from flask_socketio import SocketIO, emit, join_room, send, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from helper import *
from ttt_logic import *
import sqlite3
import os

# TODO Make board in db or json 
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
#app.config["SECRET_KEY"] = "!§)(§HOIAq38h143ui214h1)"

#TODO temp solution quick and easy make dict of the boards in for each room
rooms_board = {} 
# sessions
app.config["SESSION_PERMANENT"] = False
#socketio init
socketio = SocketIO(app)

#=========== DO NOT REPEAT ========#
def join(room):
    # check if room is already full (currently max is 2)
    # TODO make this dynamic
    with sqlite3.connect("rooms.db") as db:
        c = db.cursor()
        if get_usercount(c, room) >= 2 :
            return "room is full"
        else:
            # if not full then increase usercount in the db
            increase_usercount(c,room)
            db.commit()
 
            # add room to usser session
            session["room"] = room
            # redirect to the game
            return redirect(url_for("play"))

#================= ROUTES ====================#
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
            user =  get_user(c, username, password)
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

@app.route("/create", methods=["GET", "POST"])
def create_room():
    if request.method == "GET":
        return render_template("create_room.html")
    else:

        room = request.form.get("room")
        if not room: 
            return("No room given")

        # check if user is already in a room 
        # if he wants to reconnect reconnect-- if new room delete data from session and make him leaveleave  room
        if "room" in session:
            if session["room"] != room:
                # delete room if no one is in there
                # and decremtn usercount of that room
                with sqlite3.connect("rooms.db") as db:
                    c = db.cursor()
                    decrement_usercount(c, session.get("room"))
                    if get_usercount(c, session["room"]) == 0:
                        delete_room(c, room)
                    db.commit()

                # clear session values
                session.pop("room")


                # join room
                with sqlite3.connect("rooms.db") as db:
                    c = db.cursor()
                    if get_usercount(c, room) <=  2 :
                        # if not full then increase usercount in the db
                        increase_usercount(c,room)
                        # setting icons of the players
                        if get_usercount(c, room) == 1:
                            session["icon"] == "X"
                        else:
                            session["icon"] == "O"
                        db.commit()
 
                    else:
                        return "room is full"

                # add room to usser session
                session["room"] = room
                # redirect to the game
                return redirect(url_for("play"))

            else:
                # reconnect to room
                return redirect(url_for("play"))
 
        else:
            # first time joining TODO kinda reluctant i think
            with sqlite3.connect("rooms.db") as db:
                c = db.cursor()
                if get_usercount(c, room) <= 2 :
                    # if not full then increase usercount in the db
                    increase_usercount(c,room)
                    if get_usercount(c ,room) == 1:
                        session["icon"] = "X"
                    else:
                        session["icon"] = "O"
                    db.commit()

 
                else:
                    return "room is full"
            # add room to usser session
            session["room"] = room
            # redirect to the game
            return redirect(url_for("play"))


@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    # intitialize board this is  bad change later to be in db or json
    rooms_board[session.get("room")] = [[0 for i in range(3)]for i in range(3)]
    return render_template("play.html", room = session.get("room"), username = session.get("username") , icon = session.get("icon"))



# =================== SOCKET IO ===================================#
# when user joins game
@socketio.on('join', namespace="/play")
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(f" {username} connected {room}")

# when user makes a move
@socketio.on("move", namespace="/play")
def move(data):
    # extract y and x coordinates from json
    y = int(data["id"][0])
    x = int(data["id"][1])
    # get the room from the global array
    board = rooms_board.get(session.get("room"))
    #check if at coordinates is valid
    if board[y][x] == 0: 
        board[y][x] = session["icon"]
        # when valid send it to client where js modifies the dom 
        emit("valid", data, room = session["room"])
    else:
        emit("invalid", room = session["room"])


#@socketio.on("room_left", namespace = "/play")
def room_left(data):
    print("left")
    print("im here")
    leave_room(session.get("room"))
    session.pop("room")

# when user connects later or refresh site load board again
# !TODO! Implement later cant be bothered for that db shit right now
@socketio.on("load_board", namespace="/play")
def load_board():
    pass








if __name__ == "__main__":
    socketio.run(app, debug=True)
