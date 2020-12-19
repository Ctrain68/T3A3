from flask import Blueprint, request, jsonify, abort
from schemas.ProfileSchema import profile_schema, profiles_schema
from models.Profile import Profile
from models.Equipment import Equipment
from models.EquipmentOrder import EquipmentOrder
from models.User import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_services import verify_user
from sqlalchemy.sql import func, label
from main import db
import os
import json

from models.ProfileImages import ProfileImages
from schemas.UserSchema import user_schema, users_schema
from schemas.EquipmentSchema import equipment_schema, equipments_schema
from schemas.EquipmentOrderSchema import equipment_order_schema, equipment_orders_schema
from schemas.ProfileImagesSchema import profile_image_schema, profile_images_schema

profile = Blueprint("profile", __name__, url_prefix="/profile")

tables = ["equipment", "equipment_order", "profiles", "profile_images", "users"]
schemas = [equipments_schema, equipment_orders_schema, profiles_schema, profile_images_schema, users_schema ]




@profile.route("dump/all/<int:id>", methods=["GET"])
@jwt_required
@verify_user
def profile_dump(user, id):

    profile = db.session.query(Profile).filter(Profile.admin == True).filter_by(profileid = id, user_id=user.id).first()

    


    if not profile:
        return abort(400, description="Unauthorised to complete this action")
    i=0
    try:
        os.remove("backup/backup.json")
        print("file successfully deleted")
    except:
        print("file does not exist")
    for table in tables:
        
        
        query = db.engine.execute(f'SELECT * FROM {table}')
        data = ((schemas[i]).dump(query))


        print(data)

        data = json.dumps(data)
        i+=1
    

        file = open("backup/backup.json", "a")
        file.write(data)
        file.close()

 

    return "Data backed up"


@profile.route("/all", methods=["GET"])
def profile_index():
    query = db.session.query(Profile)

    return jsonify(profiles_schema.dump(query))


@profile.route("/active", methods=["GET"])
def profile_index_active():
 
    query = db.session.query(Profile).filter(Profile.account_active).order_by(Profile.fname)
    return jsonify(profiles_schema.dump(query))

@profile.route("/onhire", methods=["GET"])
def profile_index_profile_equipment_on_hire():

    query = db.session.query(Profile, Equipment, EquipmentOrder).outerjoin(EquipmentOrder, Profile.profileid == EquipmentOrder.hirer_id).outerjoin(Equipment, EquipmentOrder.hirer_id == Equipment.owner_id).order_by(Profile.username).all()
    things = []
    for result in query:
        things.append(f"Name: {result[0].username} Rentpw: {result[1].rentpw} Active: {result[2].order_active}")
    # print(query)
    return jsonify((things))

@profile.route("/equipment", methods=["GET"])
def profile_index_profile_equipment_rent():
    
    query = db.session.query(Profile, Equipment).join(Equipment, Profile.profileid == Equipment.owner_id ).order_by(Profile.username).all()
    things = []
    for result in query:
        things.append(f"Name: {result[0].username} Rentpw: {result[1].rentpw}")
    return jsonify(things)




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
        new_profile.admin=profile_fields["admin"]
        
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

@profile.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
@verify_user
def profile_update(user, id):


    profile = Profile.query.filter_by(profileid = id, user_id=user.id)
    
    profile_fields = profile_schema.load(request.json)

    if not profile:
        return abort(401, description="Unauthorised to update this user")
    
    
    profile.update(profile_fields)
    db.session.commit()
    
    return jsonify(profile_schema.dump(profile[0]))

@profile.route("/<int:id>", methods=["DELETE"])
@jwt_required
@verify_user
def profile_delete(user, id):


    profile = Profile.query.filter_by(profileid = id, user_id=user.id).first()


    if not profile:
        return abort(400, description="Unauthorised to delete user")
    db.session.delete(profile)
    db.session.commit()

    return jsonify(profile_schema.dump(profile))





