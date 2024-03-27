from flask import Blueprint, jsonify, request, render_template
from app import Movie, db

movielist_bp = Blueprint("movies-list", __name__)


# Get all movies
@movielist_bp.route("/")
def get_movies():
    movies_list = Movie.query.all()
    # data = [movie.to_dict() for movie in movies_list] # This makes no difference
    return render_template("movies-list.html", movies=movies_list)


# Get movie by id
@movielist_bp.route("/<movie_id>")
def get_movie_by_id(movie_id):
    filtered_movies = Movie.query.get(movie_id)
    if filtered_movies:
        return render_template("movie-detail.html", movie=filtered_movies)
    return "<h1>Movie Not Found</h1>"


# Adding new movie
@movielist_bp.route("/added", methods=["POST"])
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
@movielist_bp.route("/delete", methods=["POST"])  # HOF
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
@movielist_bp.route("/update", methods=["POST"])
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
        return "<h1> Movie updated successfully</h1>"
    except Exception as e:
        db.session.rollback()
        return f"<h1> Movie not Updated: {str(e)}</h1>"


@movielist_bp.route("/add-movie", methods=["GET"])
def add_movie_page():
    return render_template("add-movie.html")


@movielist_bp.route("/update-movie", methods=["GET", "POST"])
def update_movie_page():
    movie_id = request.form.get("movie_id")
    movie = Movie.query.get(movie_id)
    return render_template("update-movie.html", movie=movie)
