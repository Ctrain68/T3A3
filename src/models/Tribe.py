from main import db
from sqlalchemy.orm import backref
# from models.User import User

class Tribe(db.Model):
    __tablename__ ='tribes'

    id = db.Column(db.Integer, primary_key=True)
    tribe_name = db.Column(db.String(), nullable=False, unique=True)
    tribe_about = db.Column(db.String(), nullable=False)
    public = db.Column(db.Boolean(), default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    def __repr__(self):
        return f"<Tribe {self.tribename}>"