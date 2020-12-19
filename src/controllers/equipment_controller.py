from flask import Blueprint, request, jsonify, abort, render_template, url_for
from schemas.EquipmentSchema import equipment_schema, equipments_schema
from models.Equipment import Equipment
from models.Profile import Profile
from models.User import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_services import verify_user
from main import db
from sqlalchemy.sql import func, label, expression
from sqlalchemy.orm import joinedload


equipment = Blueprint("equipment", __name__, url_prefix="/equipment")

@equipment.route("/", methods=["GET"])
def equipment_get_all():
    query = db.session.query(Equipment)
    
    # return jsonify(equipments_schema.dump(query))
    return render_template("all.html", posts = query) 

@equipment.route("/available/", methods=["GET"])
def equipment_get_available():
    query = db.session.query(Equipment)
    query = query.filter(Equipment.rented == False)
    posts = query.all()
    # return jsonify(equipments_schema.dump(posts))
    return render_template("Available.html", posts = posts)   

@equipment.route("/count/", methods=["GET"])
def equipment_get_count_available():
    # query = db.session.query(Equipment)
    # equipment = query.filter(Equipment.rented == False).count().group_by()
    equipment = db.session.query(Equipment.category, label("count", func.count(Equipment.id))).filter(Equipment.rented==False).group_by(Equipment.category).order_by(Equipment.category).all()
    return jsonify(equipment)
    # posts = display.json()
    # return render_template("Categories.html", posts = equipment)  

@equipment.route("/average/", methods=["GET"])
def equipment_get_average_price(average):

    query = db.session.query(Equipment.category, label('average_rent', func.avg(Equipment.rentpw))).group_by(Equipment.category).all()
    
    return jsonify(query)
    # posts = display.json()
    # return render_template("home_page.html", posts = posts)  
   

@equipment.route("/profile", methods=["POST"])
@jwt_required
@verify_user
def equipment_create(user=None):
    
    # user = User.query.get(user_id)
    
    user_id = get_jwt_identity()

    profile = Profile.query.get(user_id)
    
    equipment_fields = equipment_schema.load(request.json)
    
    new_equipment = Equipment()
    new_equipment.equipment_name = equipment_fields["equipment_name"]
    new_equipment.equipment_description = equipment_fields["equipment_description"]
    new_equipment.category = equipment_fields["category"]
    new_equipment.rented = equipment_fields["rented"]
    new_equipment.rentpw = equipment_fields["rentpw"]
  
    
  
        
    profile.equipment.append(new_equipment)
        
    db.session.add(new_equipment)
    db.session.commit()
        
    return jsonify(equipment_schema.dump(new_equipment))




@equipment.route("/<int:id>", methods=["PUT", "PATCH"])
@jwt_required
@verify_user
def equipment_update(user, id):


    equipment = Equipment.query.filter_by(id = id, owner_id=user.id)

    equipment_fields = equipment_schema.load(request.json)

    if equipment.count() != 1:
        return abort(401, description="Unauthorised to update this Equipment")
    equipment.update(equipment_fields)


    db.session.commit()

    return jsonify(equipment_schema.dump(equipment[0]))

@equipment.route("/<int:id>", methods=["DELETE"])
@jwt_required
@verify_user
def equipment_delete(user, id):
    
    #Delete a User
    equipment = Equipment.query.options(joinedload("profile")).filter_by(id = id, owner_id=user.id).first()

    print(equipment)

    if not equipment:
        return abort(400, description="Unauthorised to delete equipment")
    db.session.delete(equipment)
    db.session.commit()

    return jsonify(equipment_schema.dump(equipment))





