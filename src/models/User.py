from main import db
from sqlalchemy.orm import backref
from models.Profile import Profile


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    profile = db.relationship("Profile", backref=backref("user", uselist=False))
    def __repr__(self):
        return f"<Users {self.email}>"