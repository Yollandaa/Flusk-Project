from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Hello, Sanlam! 😀</h1>"


@app.route("/about")
def about_page():
    return "<h1>About Page! 😀</h1>"


# if __name__ == "__main__":
#     app.route(debug=True)
