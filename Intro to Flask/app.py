import os
import json
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from dotenv import load_dotenv
from pprint import pprint
import uuid
from extensions import db

load_dotenv()  # load -> temporary as env
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FORM_SECRET_KEY"
)  # token, different for each user -> should be hidden
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

connection_String = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_String
# db = SQLAlchemy(app)

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


from movies_bp import movies_bp
from about_bp import about_bp
from movielist_bp import movielist_bp
from users_bp import users_bp
from main_bp import main_bp

app.register_blueprint(main_bp, url_prefix="/main")
app.register_blueprint(movies_bp, url_prefix="/movies")
app.register_blueprint(movielist_bp, url_prefix="/movie-list")
app.register_blueprint(about_bp, url_prefix="/about")
app.register_blueprint(users_bp, url_prefix="/users")
