import os

from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import sqlite3

app = Flask(__name__)

app.secret_key = os.environ.get("SECTRET_KEY", "dev_secret_key")

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''') 
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    task TEXT NOT NULL, user_id INTEGER REFERENCES users(id))''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    return sqlite3.connect('database.db')


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")
    
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return "Username and password are required", 400
        elif password != confirmation:
            return "Passwords do not match", 400
        
        try:
            hashed_password = generate_password_hash(password)
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except sqlite3.IntegrityError:
            return "Username already exists", 409
        
        
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

    if not username or not password:
        return "Username and password are required", 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username, ))
    user = cursor.fetchone()

    if user is None or not check_password_hash(user[2], password):
        return "Invalid username or password", 401
    else:
        session["user_id"] = user[0]
        session["username"] = user[1]
        conn.close()
        return redirect("/")
    

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")
    
    elif request.method == "POST":

        # get the task the user entered
        task = request.form.get("task")
        to_do = request.form.get("btn_to_do")

        conn = get_db()
        cursor = conn.cursor() 

        if task:
            cursor.execute("INSERT INTO tasks (status, task, user_id) VALUES (?, ?, ?)", ("to do", task, session["user_id"], ))

        if to_do:
            cursor.execute("INSERT INTO tasks (status, task, user_id) VALUES (?, ?, ?)", ("doing", to_do, session["user_id"], ))

        conn.commit()
        
        cursor.execute("SELECT task FROM tasks WHERE status = 'to do' AND user_id = ?", (session["user_id"], ))
        tasks = cursor.fetchall()

        cursor.execute("SELECT task FROM tasks WHERE status = 'doing' AND user_id = ?", (session["user_id"], ))
        doing = cursor.fetchall()

        conn.close()
        return render_template("index.html", tasks=tasks, doing=doing)

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/mood")
@login_required
def mood():     
    return render_template("mood.html") 

@app.route("/report")
@login_required
def report():
    return render_template("report.html")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)