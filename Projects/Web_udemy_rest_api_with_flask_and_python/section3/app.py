from flask import Flask
# package starts with lower case, class starts with upper case

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

app.run(port = 5000)