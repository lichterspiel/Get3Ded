from flask import Flask, render_template, redirect, request

app = Flask(__name__)

#!!!TODO!! Delete These when finished or research what they do just for debugging 
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("start.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        return "todo"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        return "todo"

@app.route("/play")
def play():
    return "todo"
