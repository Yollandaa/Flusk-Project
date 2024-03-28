from flask import Blueprint, render_template, request
from app import User, db

users_bp = Blueprint("users", __name__)


@users_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("forms.html", id="login")


@users_bp.route("/signup", methods=["GET"])
def signup_page():
    return render_template("forms.html", id="sign-up")


@users_bp.route("/logged-in", methods=["POST"])
def validate_login():
    username = request.form.get("username")
    password = request.form.get("password")
    # Get details from User where usernames are equal
    user = User.query.filter_by(username=username).first()
    if user:
        if user.password == password:
            return f"<h1>Hello, {username}</h1>"
        else:
            return f"<h1>Invalid Password</h1>"
    else:
        return f"<h1>Username not found</h1>"


@users_bp.route("/signed-in", methods=["POST"])
def sign_in():
    username = request.form.get("username")
    password = request.form.get("password")
    new_user = User(username=username, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return "<h1>Signed In Successfully</h1>"
    except Exception as e:
        db.session.rollback()
        return f"<h1>Failed to register as a user{str(e)}</h1>"
