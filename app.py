from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/mood")
def mood():     
    return render_template("mood.html") 

@app.route("/report")
def report():
    return render_template("report.html")