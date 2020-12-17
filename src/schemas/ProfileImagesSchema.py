from main import ma
from models.ProfileImages import ProfileImages
from marshmallow.validate import Length

class ProfileImagesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProfileImages

        filename = ma.String(required=True, validate=Length(min=1))

profile_image_schema = ProfileImagesSchema()
profile_images_schema = ProfileImagesSchema(many=True)