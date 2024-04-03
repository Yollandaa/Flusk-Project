import uuid

# absolute or relative import
from extensions import db  # relative import


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
