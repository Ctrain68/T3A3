from flask import Blueprint, request, jsonify, abort
from schemas.ProfileSchema import profile_schema, profiles_schema
from models.Profile import Profile
from models.Equipment import Equipment
from models.User import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_services import verify_user
from sqlalchemy.sql import func, label
from main import db

profile = Blueprint("profile", __name__, url_prefix="/profile")

@profile.route("/all", methods=["GET"])
def profile_index():
    query = db.session.query(Profile)

    return jsonify(profiles_schema.dump(query))


@profile.route("/active", methods=["GET"])
def profile_index_active():
    # query = session.query(Profile)
    query = db.session.query(Profile).filter(Profile.account_active).order_by(Profile.fname)
    return jsonify(profiles_schema.dump(query))

@profile.route("/equipment", methods=["GET"])
def profile_index_profile_equipment():
    # query = session.query(Profile)
    query = db.session.query(Profile, Equipment).outerjoin(Equipment, Profile.profileid == Equipment.owner_id).all()
    print(query)
    return jsonify(profiles_schema.dump(query))
   

@profile.route("/", methods=["POST"])
@jwt_required
@verify_user
def profile_create(user=None):
    

    user_id = get_jwt_identity()

    
    profile_fields = profile_schema.load(request.json)

    profile = Profile.query.get(user_id)

    if not profile:
    
        new_profile = Profile()
        new_profile.username = profile_fields["username"]
        new_profile.fname = profile_fields["fname"]
        new_profile.lname = profile_fields["lname"]
        new_profile.account_active=profile_fields["account_active"]
        
        user.profile.append(new_profile)
        
        db.session.add(new_profile)
        db.session.commit()
        
        return jsonify(profile_schema.dump(new_profile))
    
    else:
        return abort(401, description='User Profile already exists')

@profile.route("/<string:username>", methods=["GET"])

def profile_show(username):
    #Return a single user
    profile = Profile.query.filter_by(username = username).first()
    return jsonify(profile_schema.dump(profile))

@profile.route("/<string:username>", methods=["PUT", "PATCH"])
@jwt_required
@verify_user
def profile_update(username, user=None):


    profile = Profile.query.filter_by(username = username, user_id=user.id)

    profile_fields = profile_schema.load(request.json)

    if profile.count() != 1:
        return abort(401, description="Unauthorised to update this user")
    profile.update(profile_fields)


    db.session.commit()

    return jsonify(profile_schema.dump(profile[0]))

@profile.route("/<string:username>", methods=["DELETE"])
@jwt_required
@verify_user
def profile_delete(username, user=None):


    profile = Profile.query.filter_by(username = username, user_id=user.id).first()


    if not profile:
        return abort(400, description="Unauthorised to delete user")
    db.session.delete(profile)
    db.session.commit()

    return jsonify(profile_schema.dump(profile))





