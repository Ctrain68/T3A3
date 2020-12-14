from main import ma
from models.Profile import Profile
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema
from schemas.EquipmentSchema import EquipmentSchema

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
    username = ma.String(required=True, validate=Length(min=1))
    fname = ma.String(required=True, validate=Length(min=1))
    lname = ma.String(required=True, validate=Length(min=1))
    account_active = ma.Boolean(required=True)
    equipment = ma.Nested(EquipmentSchema)
    user = ma.Nested(UserSchema)

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)