from flask import Blueprint, request, jsonify, abort
from schemas.ProfileSchema import profile_schema, profiles_schema
from models.Profile import Profile
from models.User import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_services import verify_user
from main import db

profile = Blueprint("profile", __name__, url_prefix="/profile")

@profile.route("/", methods=["GET"])
def profile_index():
    profiles = Profile.query.all()
    return jsonify(profiles_schema.dump(profiles))
   

@profile.route("/", methods=["POST"])
@jwt_required
@verify_user
def profile_create(user=None):
    

    user_id = get_jwt_identity()

    # user = User.query.get(account_id)

    # if not account:
    #     return abort(401, description="Account not found")
    
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

    # account_id = get_jwt_identity()

    # account = Accounts.query.get(account_id)

    # if not account:
    #     return abort(401, description="Account not found")
    #Update a user

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

    # account_id = get_jwt_identity()

    # account = Accounts.query.get(account_id)

    # if not account:
    #     return abort(401, description="Account not found")

    
    #Delete a User
    profile = Profile.query.filter_by(username = username, user_id=user.id).first()

    # users_fields = user_schema.load(request.json)

    if not profile:
        return abort(400, description="Unauthorised to delete user")
    db.session.delete(profile)
    db.session.commit()

    return jsonify(profile_schema.dump(profile))





