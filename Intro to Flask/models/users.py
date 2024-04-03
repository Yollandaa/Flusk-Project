from extensions import db
import uuid


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
