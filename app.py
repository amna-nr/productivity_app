from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        to_do = request.form.get("to_do")
        doing = request.form.get("doing")
        done = request.form.get("done")

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