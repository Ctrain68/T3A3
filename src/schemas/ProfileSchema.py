from main import ma
from models.Profile import Profile
from marshmallow.validate import Length
from schemas.UserSchema import UserSchema


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        load_only = ["admin"]
    username = ma.String(required=True, validate=Length(min=1))
    fname = ma.String(required=True, validate=Length(min=1))
    lname = ma.String(required=True, validate=Length(min=1))
    admin = ma.Boolean(required=False)
    account_active = ma.Boolean(required=True)
    user = ma.Nested(UserSchema)

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)