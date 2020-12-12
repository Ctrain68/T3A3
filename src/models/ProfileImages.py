from main import db

class ProfileImages(db.Model):
    __tablename__ = 'profile_images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String())
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.profileid'), nullable=False)

    def __repr__(self):
        return f"<ProfileImage {self.id}"
