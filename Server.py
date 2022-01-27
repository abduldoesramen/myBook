from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "testing"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.permanent_session_lifetime = timedelta(minutes=5)

# Database: 
db = SQLAlchemy(app)
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, username, firstName, lastName, email):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

@app.route("/", methods=["POST", "GET"])
def home():
    # Finding out which button was pressed: 
    if request.method == "POST":
        if request.form['submit_button'] == 'Register':
            return redirect(url_for("register"))
        # Need email AND password - make valid check later:
        elif request.form['submit_button'] == 'Submit' and request.form["email"]and request.form["password"]:
            user = request.form["email"]
            session["user"] = user
            return redirect(url_for("user"))
        else:
            return render_template("index.html")
    elif request.method == "GET":
        return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        return redirect(url_for("user"))
    elif request.method == "GET":
        return render_template("register.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("register"))

if __name__ == "__main__":
    db.create_all()
    app.run(port=0)
    #python3 "Server.py"