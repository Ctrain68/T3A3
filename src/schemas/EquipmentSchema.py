from main import ma
from models.Equipment import Equipment
from schemas.ProfileSchema import ProfileSchema
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class EquipmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Equipment
    equipment_name = ma.String(required=True, validate=Length(min=1))
    equipment_description = ma.String(required=True, validate=Length(min=1))
    rented = ma.Boolean(required=True)
    rentpw = ma.Integer(required=True)
    category = ma.String(required=True, validate=Length(min=1))
    profile = ma.Nested(ProfileSchema)

equipment_schema = EquipmentSchema()
equipments_schema = EquipmentSchema(many=True)