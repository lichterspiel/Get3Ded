from flask import Flask, render_template, redirect, request, session, url_for
from flask_socketio import SocketIO, emit, join_room, send, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from helper import *
from ttt_logic import *
import sqlite3
import os
from login_blueprint import *

DB = "test.db"
# TODO Make board in db or json
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)

# blueprints
app.register_blueprint(login_blueprint)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# TODO temp solution quick and easy make dict of the boards in for each room
rooms_board = {}
# sessions
app.config["SESSION_PERMANENT"] = False
# socketio init
socketio = SocketIO(app)

#=========== DO NOT REPEAT ========#


def checker(board):
    if winner := row_check(board):
        return winner
    elif (winner := column_check(board)):
        return winner
    elif (winner := diagonal_check(board)):
        return winner
    elif (winner := diagonal2_check(board)):
        return winner
    else:
        return None

#============= Routes ================#


@app.route("/")
def index():
    return render_template("start.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
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

                with sqlite3.connect("test.db") as db:
                    c = db.cursor()
                    decrement_usercount(c, session.get("room"))
                    # deletes room only if no one is in there
                    if get_usercount(c, session["room"]) <= 1:
                        delete_room(c, session["room"])
                        rooms_board.pop(session["room"])
                    db.commit()

                # clear session values
                session.pop("room")

                # join room
                with sqlite3.connect("test.db") as db:
                    c = db.cursor()
                    join_room_s(c, room)
                    db.commit
                # add room to usser session
                session["room"] = room
                # redirect to the game
                return redirect(url_for(".play"))

            else:
                # reconnect to room
                return redirect(url_for(".play"))

        else:
            # first time joining TODO kinda reluctant i think
            with sqlite3.connect("test.db") as db:
                c = db.cursor()
                join_room_s(c, room)
                db.commit

            # add room to usser session
            session["room"] = room
            # redirect to the game
            return redirect(url_for(".play"))


@app.route("/play", methods=["GET", "POST"])
@login_required
def play():
    if request.method == "GET":

        # intitialize board this is  bad change later to be in db or json
        # check if board is already existing
        # TODO Decide if i wanna implement a reconnect
        # if session.get("room") in rooms_board:
        # return render_template("play.html", room = session.get("room"), username = session.get("username") , icon = session.get("icon"))

        # else:

        # rooms_board[session.get("room")] = [["X", "X", "X"],
        # [0,0,0],
        # [0,0,0]]

        rooms_board[session.get("room")] = [[0 for i in range(3)]
                                            for i in range(3)]
        return render_template("play.html", room=session.get("room"), username=session.get("username"), icon=session.get("icon"))

    else:
        return redirect(url_for(".index"))

#=================== SOCKET IO ===================================#

# when user joins game
@socketio.on('join', namespace="/play")
def on_join(data):

    # if the user was already in a room leave it
    # currently not WORKING TODO because the room in the session is the true room not the old but it kinda works cuz i just need the to join the room
    # save the old room when joining a new one

    # if session["room"]:
    # leave_room(session.get("room"))

    # extract the data
    username = data['username']
    room = data['room']
    join_room(room)
    # tell the client that it can now get the board data
    emit("start_loading", room=room)
    print(f" {username} connected {room}")

# when user makes a move

@socketio.on("move", namespace="/play")
def move(data):
    with sqlite3.connect("test.db") as db:
        c = db.cursor()
        if not isTurn(c, session.get("room")) or get_usercount(c, session.get("room")) != 2:
            return

    print("§")
    # extract y and x coordinates from json
    y = int(data["id"][0])
    x = int(data["id"][1])
    # get the room from the global array
    board = rooms_board.get(session.get("room"))
    # check if at coordinates is valid
    if board[y][x] == 0:
        board[y][x] = session["icon"]
        print(board)
        # when valid send it to client where js modifies the dom
        emit("valid", data, room=session["room"])

        # TIC TAC TOE LOGIC check the rows and column if won

        if checker(board) != None:
            print("herer")
            winner = str(checker(board))
            print(f"winner is {winner}")
            emit("Winner", {"winner": winner}, room=session["room"])
        with sqlite3.connect("test.db") as db:
            c = db.cursor()
            change_turn(c, session.get("room"))
            db.commit()
    else:
        emit("invalid", room=session["room"])
        


@socketio.on("game_finished", namespace="/play")
def game_finished(data):
    with sqlite3.connect(DB) as db:
        c = db.cursor()
        delete_room_e(c, data["room"])

        rooms_board.pop(data["room"])
        session.pop("room")
        # TODO update user stats

        db.commit()

# load the board when user joins when he left before finishing the game
# TODO change this when changing how i store the board data


@socketio.on("load_board", namespace="/play")
def load_board():
    board = rooms_board.get(session.get("room"))
    if board:
        # i parse an array is this bad ? TODO
        # give the client the board data
        emit("load", board, room=session.get("room"))


#=============START THE APP===========#

if __name__ == "__main__":
    socketio.run(app, debug=True)
