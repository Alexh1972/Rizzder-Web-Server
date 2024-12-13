import ast
from PIL import Image
from flask import Flask, request, render_template, redirect, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_folder="public")

session = {"authenticated": False, "username": ""}

ALLOWED_USERS = {"admin": "admin"}

wallpapers = {}

DATABASE_FILE = "public/database.txt"

@app.route("/")
def index():
    return render_template("index.html", wallpapers=wallpapers, session=session)

@app.route('/about')
def about():
    return render_template('about.html', session=session)

@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if ALLOWED_USERS.get(username) == password:
            session["authenticated"] = True
            session["username"] = username
            return redirect("/")
        else:
            error_msg = "Wrong username or password. Please try again."
            pass
    return render_template("login.html", session=session, error_msg=error_msg)

@app.route("/logout")
def logout():
    if not session["authenticated"]:
        return redirect("/")

    session["authenticated"] = False
    session["username"] = ""
    return redirect("/")

@app.errorhandler(404)
def error404(code):
    return "HTTP Error 404 - Page Not Found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

