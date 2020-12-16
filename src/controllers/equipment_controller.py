from flask import Blueprint, request, jsonify, abort, render_template, url_for
from schemas.EquipmentSchema import equipment_schema, equipments_schema
from models.Equipment import Equipment
from models.Profile import Profile
from models.User import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_services import verify_user
from main import db
from sqlalchemy.sql import func, label, expression
import json

equipment = Blueprint("equipment", __name__, url_prefix="/")


@equipment.route("/available/<string:available>", methods=["GET"])
def equipment_get_available(available):
    query = db.session.query(Equipment)
    query = query.filter(Equipment.rented == False)
    posts = query.all()
    return jsonify(equipments_schema.dump(posts))
    # return render_template("home_page.html", posts = posts)   

@equipment.route("/count/<string:count>", methods=["GET"])
def equipment_get_count_available(count):
    # query = db.session.query(Equipment)
    # equipment = query.filter(Equipment.rented == False).count().group_by()
    equipment = db.session.query(Equipment.category, label("count", func.count(Equipment.id))).filter(Equipment.rented==False).group_by(Equipment.category).order_by(Equipment.category).all()
    return jsonify(equipment)
    # posts = display.json()
    # return render_template("home_page.html", posts = posts)  

@equipment.route("/average/<string:average>", methods=["GET"])
def equipment_get_average_price(average):
    # query = Equipment.query(func.sum(Equipment.rentpw.all()))
    query = db.session.query(Equipment.category, label('average_rent', func.avg(Equipment.rentpw))).group_by(Equipment.category).all()
    
    # query = db.session.query(func.avg(Equipment.rentpw).label("average_rent")).group_by(Equipment.rented).all()
    # equipment = query.filter(Equipment.rented == False).count()
    # equipment = query.all()
    return jsonify(query)
    # posts = display.json()
    # return render_template("home_page.html", posts = posts)  

# @tribe.route("/<string:tribe_name>", methods=["GET"])
# def tribe_tribe_name():
#     tribes = Tribe.query.filter_by(tribe_name = tribe_name).first()
#     return jsonify(tribe_schema.dump(tribes))

# @tribe.route("/", methods=["GET"])
# def tribe_index():
#     tribes = Tribe.query.all()
#     return jsonify(tribes_schema.dump(tribes))
   

# @tribe.route("/", methods=["POST"])
# @jwt_required
# @verify_user
# def tribe_create(user=None):
    

#     user_id = get_jwt_identity()

#     # user = User.query.get(account_id)

#     # if not account:
#     #     return abort(401, description="Account not found")
    
#     tribe_fields = tribe_schema.load(request.json)

#     # tribe = Tribe.query.get(user_id)

#     # if not profile:
    
#     new_tribe = Tribe()
#     new_tribe.tribe_name = tribe_fields["tribe_name"]
#     new_tribe.tribe_about = tribe_fields["tribe_about"]
#     new_tribe.public = tribe_fields["public"]
  
        
#     user.tribe.append(new_tribe)
        
#     db.session.add(new_tribe)
#     db.session.commit()
        
#     return jsonify(tribe_schema.dump(new_tribe))
    
#     # else:
#     #     return abort(401, description='User Profile already exists')

# @tribe.route("/<string:public>", methods=["GET"])

# def tribe_show(public):
#     query = db.session.query(Tribe)
#     query = query.filter(Tribe.public == True)
#     tribes = query.all()
#     return jsonify(tribes_schema.dump(tribes))

# @tribe.route("/<string:tribe_name>", methods=["PUT", "PATCH"])
# @jwt_required
# @verify_user
# def tribe_update(tribe_name, user=None):


#     tribe = Tribe.query.filter_by(tribe_name = tribe_name, user_id=user.id)

#     tribe_fields = tribe_schema.load(request.json)

#     if tribe.count() != 1:
#         return abort(401, description="Unauthorised to update this Tribe")
#     tribe.update(tribe_fields)


#     db.session.commit()

#     return jsonify(tribe_schema.dump(tribe[0]))

# @profile.route("/<string:username>", methods=["DELETE"])
# @jwt_required
# @verify_user
# def profile_delete(username, user=None):

#     # account_id = get_jwt_identity()

#     # account = Accounts.query.get(account_id)

#     # if not account:
#     #     return abort(401, description="Account not found")

    
#     #Delete a User
#     profile = Profile.query.filter_by(username = username, user_id=user.id).first()

#     # users_fields = user_schema.load(request.json)

#     if not profile:
#         return abort(400, description="Unauthorised to delete user")
#     db.session.delete(profile)
#     db.session.commit()

#     return jsonify(profile_schema.dump(profile))





