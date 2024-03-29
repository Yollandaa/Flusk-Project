import os
import json
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
from pprint import pprint
import uuid

load_dotenv()  # load -> temporary as env
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FORM_SECRET_KEY"
)  # token, different for each user -> should be hidden
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

connection_String = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_String
db = SQLAlchemy(app)

# Model (SQLAlchemy) == Schema

# CREATE TABLE movies (
#     id VARCHAR(50) PRIMARY KEY,
#     name VARCHAR(100),
#     poster VARCHAR(255),
#     rating FLOAT,
#     summary VARCHAR(500),
# 	trailer VARCHAR(255)
# );


class Movie(db.Model):
    # Table name we pointing it to
    __tablename__ = "movies"
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100))
    poster = db.Column(db.String(255))
    rating = db.Column(db.Float)
    summary = db.Column(db.String(500))
    trailer = db.Column(db.String(255))

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "poster": self.poster,
            "rating": self.rating,
            "summary": self.summary,  # Naming it whatever you want
            "trailer": self.trailer,
        }


# Task - User Model | id, username, password
# Sign Up page
# Login page
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }


try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        # db.create_all()  # This creates the table if it diesn't exist in the mssm database
except Exception as e:
    print("Error connecting to the database:", e)

# local
# /dashboard

# jinja2 - template
# What python gives you to manipulate your html
# Improves DX

name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming", "Yoga"]


@app.route("/")
def hello_world():
    return "<h1>Hello, Sanlam! 😀</h1>"


@app.route("/profile")
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)


from movies_bp import movies_bp
from about_bp import about_bp
from movielist_bp import movielist_bp
from users_bp import users_bp

app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(movielist_bp, url_prefix="/movie-list")
app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(users_bp, url_prefix="/users")
