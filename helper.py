import sqlite3
from flask import redirect, render_template, request, session, url_for
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None: 
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function 

# is it better to connec once or every time function is called 
# connect to database
#db = sqlite3.connect("test.db")

# create cursor to execute SQL querys
#c = db.cursor()

# return 0 for success
def create_database(c):
    c.execute('''CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER UNIQUE,
	"username"	TEXT UNIQUE,
	"password"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
    )''')
    return 0
    
def register_user(c,username, password):
    # ? needs to take in a tuple
    # check if username and password is not empty
    if username and password:
        # check if username doesnt exist
        user = c.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user != None:
            return False 
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username,password))
            return True
    else:
        return False

    
def get_user(c,username, password):
    user = c.execute("SELECT password FROM users WHERE username=?", (username,)).fetchone()    
    return user

def increase_usercount(c, room):
    user_count = c.execute("SELECT user_count FROM rooms WHERE room = ?", (room,)).fetchone()
    if user_count != None:
        user_count = int(user_count[0])
        c.execute("UPDATE rooms SET user_count = ? WHERE room = ?", (user_count + 1, room))
    else:
        c.execute("INSERT INTO rooms (room, user_count, p1, p2, turn) VALUES (?, ?, ?, ?, ?)", (room, 1, 0, 0, 0))

def decrement_usercount(c,room):
    user_count = c.execute("SELECT user_count FROM rooms WHERE room = ?", (room,)).fetchone()
    if user_count != None:
        user_count = int(user_count[0])
        c.execute("UPDATE rooms SET user_count = ? WHERE room = ?", (user_count - 1, room))

def get_usercount(c, room):
    user_count = c.execute("SELECT user_count FROM rooms WHERE room = ?", (room,)).fetchone()
    if user_count == None:
        return 0
    else:
        return user_count[0]


def delete_room(c, room):
    if get_usercount(c,room) == 0:
        c.execute("DELETE FROM rooms WHERE room = ?", (room,))

def join_room_s(c, room):
    if get_usercount(c, room) < 2:
        # if not full then increase usercount in the db
        increase_usercount(c,room)
        if get_usercount(c, room) == 1:
            # set icon of player
            session["icon"] = "X"
            # Add to db the user whose turn it is

            c.execute("UPDATE rooms SET turn = ? , p1 = ? WHERE room = ?", (session.get("username"), session.get("username"), room))
        else:
            session["icon"] = "O"
            c.execute("UPDATE rooms SET p2 = ? WHERE room = ?", (session.get("username"), room))
    else:
        return "room is full"

def isTurn(c, room):
    # see whose turn it is
    turn = c.execute("SELECT turn FROM rooms WHERE room = ?", (room,)).fetchone()

    # if it is your turn return true else return false
    return turn[0] == session.get("username")

def change_turn(c, room):
    # TODO add all users to the db
    current_turn = c.execute("SELECT turn FROM rooms WHERE room = ?", (session.get("room"),)).fetchone()
    p1 = c.execute("SELECT p1 FROM rooms WHERe room = ?", (session.get("room"),)).fetchone()
    p2 = c.execute("SELECT p2 FROM rooms WHERe room = ?", (session.get("room"),)).fetchone()

    if p1[0] == current_turn[0]: 
        # change turn from player 1 to player 2
        c.execute("UPDATE rooms SET turn = ? WHERE room = ?", (p2[0], room))
    else:
        # change turn from player 2 to player 1
        c.execute("UPDATE rooms SET turn = ? WHERE room = ?",(p1[0], room))
