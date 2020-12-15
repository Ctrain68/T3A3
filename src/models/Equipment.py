from main import db
from sqlalchemy.orm import backref
from models.EquipmentOrder import EquipmentOrder


class Equipment(db.Model):
    __tablename__ ='equipment'

    id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.String(), nullable=False, unique=True)
    equipment_description = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    rented = db.Column(db.Boolean(), default=False)
    rentpw = db.Column(db.Integer(), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("profiles.profileid"), nullable=False)
    equipment_order = db.relationship("EquipmentOrder", backref="equipment")
    def __repr__(self):
        return f"<Equipment {self.equipment_name}>"