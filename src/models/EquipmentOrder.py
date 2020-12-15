from main import db
from sqlalchemy.orm import backref
from datetime import datetime


class EquipmentOrder(db.Model):
    __tablename__ ='equipment_order'

    equipmentorderid = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey("equipment.id"), nullable=False)
    hirer_id = db.Column(db.Integer, db.ForeignKey("profiles.profileid"), nullable=False)
    order_begin_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    order_return_date_estimate = db.Column(db.DateTime, nullable=True)
    order_actual_return_date = db.Column(db.DateTime, nullable=True)
    order_active = db.Column(db.Boolean(), default=True)
    
    
    
    def __repr__(self):
        return f"<Order {self.equipmentorderid}>"