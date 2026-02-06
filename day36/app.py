from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", message="Welcome Friend!")

@app.route("/greet/<name>")
def greet(name):
    name = name.title()
    return render_template("greet.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)