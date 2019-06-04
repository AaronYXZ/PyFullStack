from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    user_agent = request.headers.get("User-Agent")
    return "<h1> hello world</h1> <h2>your user agent is {}</h2>".format(user_agent)

@app.route("/user/<name>")
def user(name):
    return "<h1>hello, %s</h1>" % name

if __name__ == '__main__':
    app.run(debug = False)