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
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

connection_String = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_String
db = SQLAlchemy(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)

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


# Get all movies
@app.route("/movies-list")
def get_movies():
    movies_list = Movie.query.all()
    # data = [movie.to_dict() for movie in movies_list] # This makes no difference
    return render_template("movies-list.html", movies=movies_list)


# Get movie by id
@app.route("/movie-list/<movie_id>")
def get_movie_by_id(movie_id):
    filtered_movies = Movie.query.get(movie_id)
    if filtered_movies:
        return render_template("movie-detail.html", movie=filtered_movies)
    return "<h1>Movie Not Found</h1>"


# Adding new movie
@app.route("/movie-added", methods=["POST"])
def create_movie():
    name = request.form.get("name")
    poster = request.form.get("poster")
    rating = request.form.get("rating")
    summary = request.form.get("summary")
    trailer = request.form.get("trailer")

    new_movie = Movie(
        name=name, poster=poster, rating=rating, summary=summary, trailer=trailer
    )
    try:
        db.session.add(new_movie)
        db.session.commit()
        return render_template("movies-list.html", movies=Movie.query.all())
    except Exception as e:
        db.session.rollback()
        return f"<h1>Create Failed {str(e)}</h1>", 500


# Delete Movie
@app.route("/movie-list/delete", methods=["POST"])  # HOF
def delete_movie_by_id():
    movie_id = request.form.get("movie_id")
    filtered_movie = Movie.query.get(movie_id)  # get the movie first
    if not filtered_movie:
        return "<h1>Movie Not Found</h1>", 404
    try:
        db.session.delete(filtered_movie)
        db.session.commit()
        return "<h1>Movie deleted Successfully</h1>"
    except Exception as e:
        db.session.rollback()
        return f"<h1>Delete Failed {str(e)}</h1>", 500


#  Update a movie
@app.route("/movies/update", methods=["POST"])
def update_movie_by_id():
    movie_id = request.form.get("movie_id")
    print("This is the id: ", movie_id)
    filtered_movie = Movie.query.get(movie_id)
    update_data = {}
    # Get the data via request.form.get
    if request.form.get("name"):
        update_data["name"] = request.form.get("name")
    if request.form.get("poster"):
        update_data["poster"] = request.form.get("poster")
    if request.form.get("rating"):
        update_data["rating"] = request.form.get("rating")
    if request.form.get("summary"):
        update_data["summary"] = request.form.get("summary")
    if request.form.get("trailer"):
        update_data["trailer"] = request.form.get("trailer")

    if not filtered_movie:
        return "<h1> Movie Not Found</h1>"

    try:
        for key, value in update_data.items():
            if hasattr(filtered_movie, key):
                setattr(filtered_movie, key, value)
        db.session.commit()
        return
    except Exception as e:
        db.session.rollback()
        return f"<h1> Movie not Updated: {str(e)}</h1>"


# local
# /dashboard

# jinja2 - template
# What python gives you to manipulate your html
# Improves DX

name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming", "Yoga"]

users = [
    {
        "name": "Gemma",
        "pic": "https://th.bing.com/th/id/OIP.rS1lWWgFD0gV-nbP2XxdVgAAAA?w=416&h=315&rs=1&pid=ImgDetMain",
        "pro": True,
    },
    {
        "name": "Lilitha",
        "pic": "https://th.bing.com/th/id/OIP.ZP-E8ZFH11wb1XSm0dn-5wHaJQ?rs=1&pid=ImgDetMain",
        "pro": False,
    },
    {
        "name": "Caleb",
        "pic": "https://cdn.lifehack.org/wp-content/uploads/2015/02/what-makes-people-happy.jpeg",
        "pro": True,
    },
]


@app.route("/")
def hello_world():
    return "<h1>Hello, Sanlam! 😀</h1>"


@app.route("/profile")
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)


@app.route("/base")
def about_page():
    return render_template("about.html", users=users)


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("forms.html")


@app.route("/dashboard", methods=["POST"])
def dashboard_page():
    username = request.form.get("username")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return f"<h1>Hello, {username}</h1>"
    # return render_template("dashboard.html")


@app.route("/add-movie", methods=["GET"])
def add_movie_page():
    return render_template("add-movie.html")


@app.route("/update-movie", methods=["GET", "POST"])
def update_movie_page():
    movie_id = request.form.get("movie_id")
    movie = Movie.query.get(movie_id)
    return render_template("update-movie.html", movie=movie)


#  ---------------- POSTMAN STUFF --------------------------------

# Creating new movie
# @app.post("/movies")
# def add_movie():
#     data = request.json
#     new_movie = Movie(
#         **data
#     )  # Rule the keys must be the same, if there's id (that one will be choosen)
#     try:
#         db.session.add(new_movie)
#         db.session.commit()
#         result = {"message": "Movie added successfully", "data": new_movie.to_dict()}
#     except Exception as e:
#         db.session.rollback()
#         result = {"message": "Movie failed to Add", "error": str(e)}
#     return jsonify(result), 500


# Update method to update movie by id for postman
# @app.put("/movies/<movie_id>")
# def update_movie_by_id(movie_id):
#     filtered_movie = Movie.query.get(movie_id)
#     update_data = request.json
#     print(type(update_data))

#     if not filtered_movie:
#         return "<h1>Movie Not Found</h1>"

#     try:
#         # filtered_movie.name = update_data.get("name", filtered_movie.name)
#         # filtered_movie.poster = update_data.get("poster", filtered_movie.poster)
#         # filtered_movie.rating = update_data.get("rating", filtered_movie.rating)
#         # filtered_movie.summary = update_data.get("summary", filtered_movie.summary)
#         # filtered_movie.trailer = update_data.get("trailer", filtered_movie.trailer)

#         # Shorten the above
#         for key, value in update_data.items():
#             if hasattr(filtered_movie, key):
#                 setattr(filtered_movie, key, value)

#         db.session.commit()
#         return jsonify(filtered_movie.to_dict())
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)})
