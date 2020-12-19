from models.ProfileImages import ProfileImages
from models.Profile import Profile
from schemas.ProfileImagesSchema import profile_image_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort, current_app, Response
from services.auth_services import verify_user
from pathlib import Path
from main import db
import boto3


profile_images = Blueprint('profile_images', __name__, url_prefix="/profile/<int:profile_id>/image")

@profile_images.route("/", methods=["POST"])
@jwt_required
@verify_user
def profile_image_create(profile_id, user=None):
    profile = Profile.query.filter_by(profileid=profile_id, user_id=user.id).first()
    
    if not profile:
        return abort(401, description="Invalid user")

    # if users.count() != 1:
    #     return abort(401, description="Invalid User")
    
    if "image" not in request.files:
        return abort(400, description="Missing image")

    image = request.files["image"]

    if Path(image.filename).suffix not in [".png", ".tif", ".jpg", ".gif"]:
        return abort(402, description="Invalid file type")
    
    filename = f"{profile_id}{Path(image.filename).suffix}"
    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    key = f"profile_images/{filename}"

    bucket.upload_fileobj(image, key)

    if not profile.profile_image:
        new_image = ProfileImages()
        new_image.filename = filename
        profile.profile_image = new_image
        db.session.commit()
    
    return ("Ok", 201)

@profile_images.route("/<int:id>", methods=["GET"])
def profile_image_show(profile_id, id):
    profile_image = ProfileImages.query.filter_by(id=id).first()

    if not profile_image:
        return abort(401, description="Invalid user")

    bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
    filename = profile_image.filename
    file_obj = bucket.Object(f"profile_images/{filename}").get()

    print(file_obj)

    return Response(
        file_obj["Body"].read(),
        mimetype="image/*",
        headers={"Content-Disposition": "attachment;filename=image"}
    )


@profile_images.route("/<int:id>", methods=["DELETE"])
@jwt_required
@verify_user
def profile_image_delete(profile_id, id, user=None):
    profile = Profile.query.filter_by(profileid=profile_id, user_id=user.id).first()

    if not profile:
        return abort(401, description="Invalid book")
    
    if profile.profile_image:
        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        filename = profile.profile_image.filename

        bucket.Object(f"profile_images/{filename}").delete()

        db.session.delete(profile.profile_image)
        db.session.commit()

    return ("OK", 204)




#     # if "image" in request.files:
#     #     image = request.files["image"]
#     #     image.save("uploaded_images/file_1")
#     #     return ("", 200)
#     # return abort(400, description="No Image")

# @profile_images.route("/<int:id>", methods=["GET"])
# def book_image_show(user_id, id):
#     pass

# @profile_images.route("/<int:id>", methods=["DELETE"])
# @jwt_required
# def profile_image_delete(user_id, id):
#     pass