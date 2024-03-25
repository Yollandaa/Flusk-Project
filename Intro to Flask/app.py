import json
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

movies = [
    {
        "id": "99",
        "name": "Vikram",
        "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
        "rating": 8.4,
        "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
        "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
    },
    {
        "id": "100",
        "name": "RRR",
        "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
        "rating": 8.8,
        "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
        "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
    },
    {
        "id": "101",
        "name": "Iron man 2",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
        "rating": 7,
        "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
        "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
    },
    {
        "id": "102",
        "name": "No Country for Old Men",
        "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
        "rating": 8.1,
        "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
        "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
    },
    {
        "id": "103",
        "name": "Jai Bhim",
        "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
        "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
        "rating": 8.8,
        "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
    },
    {
        "id": "104",
        "name": "The Avengers",
        "rating": 8,
        "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
        "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
        "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
    },
    {
        "id": "105",
        "name": "Interstellar",
        "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
        "rating": 8.6,
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
    },
    {
        "id": "106",
        "name": "Baahubali",
        "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
        "rating": 8,
        "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
        "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
    },
    {
        "id": "107",
        "name": "Ratatouille",
        "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
        "rating": 8,
        "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
        "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
    },
    {
        "name": "PS2",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
        "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
        "rating": 8,
        "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
        "id": "108",
    },
    {
        "name": "Thor: Ragnarok",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
        "rating": 8.8,
        "trailer": "https://youtu.be/NgsQ8mVkN8w",
        "id": "109",
    },
]

# jinja2 - template
# What python gives you to manipulate your html
# Improves DX

user = {
    "name": "Yolanda",
    "pic": "https://mail.google.com/mail/u/0?ui=2&ik=7298456c45&attid=0.1&permmsgid=msg-a:r-342784761304772687&th=18e5b959384ae45d&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ-A2WeYZ77wdd62sQEzaQy_2xN6ZxVK9tWxztozwbJNXVyuR6YoOj_3hzFPmG97Z-75KTqay9smb16ByNU8mfIDNDucF9sMOCrD6M0Zh-OzZUWtDFwhL02C18Q&disp=emb&realattid=ii_ltzplwc30",
}

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


# Create dashboard page to list the movies
@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html", movies=movies)


# /movies -> json
@app.get("/movies")
def get_movies():
    return jsonify(movies)


# post method to add movies
@app.post("/movies")
def add_movie():
    new_movie = request.json
    # edit the new movie so that the id is the max_id + 1 from the movies_list
    new_movie["id"] = max_plus_one()
    movies.append(new_movie)
    return jsonify(new_movie)


def max_plus_one():
    max_id = max([int(movie["id"]) for movie in movies])
    return str(max_id + 1)


# Get method to get movie by id
# <variable_name> | movie_id becomes the keyword arguement
# Generator expression -> returns the first match only
# -> The loop stops as soon as the first match is found
# @app.get("/movies/<movie_id>")
# def get_movie_by_id(movie_id):
#     filtered_movies = next((movie for movie in movies if movie["id"] == movie_id), None)
#     if filtered_movies:
#         return jsonify(filtered_movies)
#     return jsonify({"Error": "Movie not found"}), 404


# Get method to get movie by id for frontend
@app.get("/movies/<movie_id>")
def get_movie_by_id(movie_id):
    filtered_movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    if filtered_movie:
        return render_template("movie-detail.html", movie=filtered_movie)
    return "<h1>Movie not found</h1>"


# Delete method to delete movie by id
# @app.delete("/movies/<movie_id>")
# def delete_movie_by_id(movie_id):
#     filtered_movie = next((movie for movie in movies if movie["id"] == movie_id), None)
#     if filtered_movie:
#         movies.remove(filtered_movie)
#         return jsonify(filtered_movie)
#     return jsonify({"Error": "Movie not found"}), 404


@app.delete("/movies/<movie_id>")
def delete_movie_by_id(movie_id):
    filtered_movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    if filtered_movie:
        movies.remove(filtered_movie)
        return jsonify(filtered_movie)
    return jsonify({"Error": "Movie not found"}), 404


# Update method to update movie by id
@app.put("/movies/<movie_id>")
def update_movie_by_id(movie_id):
    filtered_movie = next((movie for movie in movies if movie["id"] == movie_id), None)
    update_data = request.json
    if filtered_movie:
        filtered_movie.update(update_data)
        return jsonify(filtered_movie)
    return jsonify({"Error": "Movie not found"}), 404


# @app.put("/movies/<id>")
# def update_movie_by_id(id):
#     movie_idx = next((idx for idx, movie in enumerate(movies) if movie["id"] == id), None) # same memory
#     body = request.json
#     movies[movie_idx] = {**movies[movie_idx], **body}


# if __name__ == "__main__":
#     max_plus_one()
#     app.run(debug=True)
