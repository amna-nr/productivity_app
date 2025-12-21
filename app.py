from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

conn = sqlite3.connect("database.db") # connect to the database
db = conn.cursor() # to be able to execute SQL commands

# create users table
db.execute("""CREATE TABLE 
            IF NOT EXISTS users 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL, 
            password_hash TEXT NOT NULL)""")

# create tasks table
db.execute("""CREATE TABLE 
            IF NOT EXISTS tasks
            (task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            status TEXT NOT NULL,
           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id))""")

conn.commit()
conn.close()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        to_do = request.form.get("to_do")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/mood")
def mood():     
    return render_template("mood.html") 

@app.route("/report")
def report():
    return render_template("report.html")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)