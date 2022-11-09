from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.cyclist import Cyclist
from .routes_helper import get_one_obj_or_abort
from app.models.bike import Bike

cyclist_bp = Blueprint("cyclist__bp", __name__, url_prefix="/cyclist")

@cyclist_bp.route("", methods=["GET"]) # decorator - telling flask when a request comes in, use this function
# then methods=["GET"] says if it uses /cyclist and uses GET method, flask will know where everything goes
# method has to be a list!
# url_prefix = "/bike" helps with the path 

def get_all_cyclists(): # want it to return JSON eventually to the client
    cyclist = Cyclist.query.all()
    
    response = [cyclist.to_dict() for cyclist in cyclist]
    return jsonify(response), 200 

@cyclist_bp.route("/<cyclist_id>/bike", methods=["GET"])
def get_all_bikes_belonging_to_a_cyclist(cyclist_id):
    cyclist = get_one_obj_or_abort(Cyclist, cyclist_id)

    bikes_response = [bike.to_dict() for bike in cyclist.bikes]

    return jsonify(bikes_response), 200

@cyclist_bp.route("/<cyclist_id>/bike", methods=["POST"])
def post_bike_belonging_to_cyclist(cyclist_id):
    parent_cyclist = get_one_obj_or_abort(Cyclist, cyclist_id)

    request_body = request.get_json()

    new_bike = Bike.from_dict(request_body)
    # link new bike to cyclist it belongs to
    new_bike.cyclist = parent_cyclist # sets cyclist attribute to whatever parent cyclist from above
    # SQLAlchemy will recognize this and populate the relationship

    db.session.add(new_bike)
    db.session.commit()

    return jsonify({"message": f"Bike {new_bike.name} belonging to {new_bike.cyclist.name} successfully added"}), 201