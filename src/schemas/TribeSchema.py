from main import ma
from models.Tribe import Tribe
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema

class TribeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tribe
    tribe_name = ma.String(required=True, validate=Length(min=1))
    tribe_about = ma.String(required=True, validate=Length(min=1))
    public = ma.Boolean(required=True)
    user = ma.Nested(UserSchema)

tribe_schema = TribeSchema()
tribes_schema = TribeSchema(many=True)