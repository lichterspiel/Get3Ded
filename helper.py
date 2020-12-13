import sqlite3

# is it better to connec once or every time function is called 
# connect to database
db = sqlite3.connect("test.db")

# create cursor to execute SQL querys
c = db.cursor()

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

print(get_user(c,"34",1))
