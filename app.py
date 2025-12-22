from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''') 
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (task_id INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    task TEXT NOT NULL, user_id INTEGER REFERENCES users(id))''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    return sqlite3.connect('database.db')

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