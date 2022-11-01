from flask import Blueprint, jsonify, request, abort, make_response
from app import db
# from app.models import bike
from app.models.bike import Bike 

bike_bp = Blueprint("bike__bp", __name__, url_prefix="/bike") # then create instance of the blueprint class - make it a string to refer to it later

# don't want to hardcode bike data but want client to be able to
# adding many different routes below that match the bp above (we register the routes to match to that)

def get_one_bike_or_abort(bike_id): # helper function so doesn't have decorator so client cannot access
    try: # don't need a decorator because we are calling it later and don't need an http route or method for it
        bike_id = int(bike_id)
    except ValueError: 
        response_str = f"Invalid bike_id: '{bike_id}'. ID must be an integer."
        abort(make_response(jsonify({"message":response_str})), 400)
    
    matching_bike = Bike.query.get(bike_id)

    if matching_bike is None: # could also use "if not matching_bike:" for falsey 
        response_str = f"Bike with id '{bike_id}' was not found in the database."
        abort(make_response(jsonify({"message":response_str})), 404)
    
    return matching_bike

@bike_bp.route("", methods=["POST"])

def add_bike():
    request_body = request.get_json()

    new_bike = Bike(
        name=request_body["name"],
        price=request_body["price"],
        size=request_body["size"],
        type=request_body["type"]
    )

    db.session.add(new_bike)
    db.session.commit() # CRUCIAL!!!!!! must do a commit here for the addition
    # we do commits when we are making a change to our db
    # we don't change anything with the helper function above so do not need to commit it

    return {"id": new_bike.id}, 201 # if only change routes or models, don't need to do upgrade 

@bike_bp.route("", methods=["GET"]) # decorator - telling flask when a request comes in, use this function
# then methods=["GET"] says if it uses /bikes and uses GET method, flask will know where everything goes
# method has to be a list!
# url_prefix = "/bike" helps with the path 

def get_all_bikes(): # want it to return JSON eventually to the client
    name_param = request.args.get("name") # putting name of query param in there "name"
    
    if name_param is None: # if they do not put in the parameter/name filter, we do the normal query.all
        bikes = Bike.query.all()
    else:
        bikes = Bike.query.filter_by(name=name_param)

    response = []
    for bike in bikes:
        bike_dict = {
            "id": bike.id,
            "name": bike.name,
            "price": bike.price,
            "size": bike.size,
            "type": bike.type      
        }
        response.append(bike_dict)
    return jsonify(response), 200 
    # using jsonify (imported from flask) will translate it to json for ... and 200 is the status code



@bike_bp.route("/<bike_id>", methods=["GET"]) # route parse then convert to an int - using <> with user input inside

def get_one_bike(bike_id): # put bike_id as an argument to connect with get method above
    chosen_bike = get_one_bike_or_abort(bike_id)
    bike_dict = {
            "id": chosen_bike.id,
            "name": chosen_bike.name,
            "price": chosen_bike.price,
            "size": chosen_bike.size,
            "type": chosen_bike.type      
        }
    return jsonify(bike_dict), 200 # can use to_dict to convert to dict in case it's not already in dict format

@bike_bp.route("/<bike_id>", methods=["PUT"])

def update_bike_with_new_vals(bike_id):
    
    chosen_bike = get_one_bike_or_abort(bike_id)
    
    request_body = request.get_json()

    if "name" not in request_body or \
        "size" not in request_body or \
        "price" not in request_body or \
        "type" not in request_body:
            return jsonify({"message": "Request must include name, size, price, and type"}), 400
    
    chosen_bike.name = request_body["name"]
    chosen_bike.size = request_body["size"]
    chosen_bike.price = request_body["price"]
    chosen_bike.type = request_body["type"]

    db.session.commit()

    return jsonify({"message": "Successfully replaced bike with id '{bike_id}'"}), 200

@bike_bp.route("/<bike_id>", methods=["DELETE"])
def delete_one_bike(bike_id):
    chosen_bike = get_one_bike_or_abort(bike_id)
    
    db.session.delete(chosen_bike)

    db.session.commit()

    return jsonify({"message": "Successfully deleted bike with id '{bike_id}'"}), 200

    '''
    try:
        bike_id = int(bike_id)
    except ValueError: 
        response_str = f"Invalid bike_id: '{bike_id}'. ID must be an integer."
        return jsonify({"message": response_str}), 400

    # try-except: try to convert o an int, if error occurs, catch it and raise 400 error with msg
    # after the try-except: bike_id will be a valid in
    # loop through data to find a bike w/ matching bike_id 
    # if found: return that bike's data with 200 code
    for bike in bikes:
        if bike.id == bike_id:
            bike_dict = {
            "id": bike.id,
            "name": bike.name,
            "price": bike.price,
            "size": bike.size,
            "type": bike.type      
            }
            return jsonify(bike_dict), 200 # return in if block 
    # after the loop: the bike w/ matching bike_id was not found, we will raise 404 error with msg
    response_message = f"Could not find bike with this ID {bike_id}"
    return jsonify({"message": response_message}), 404

'''




'''class Bike:
    def __init__(self, id, name, price, size, type): # create constructor method 
        self.id = id
        self.name = name
        self.price = price
        self.size = size
        self.type = type


    bikes = [
    
    Bike(5, "Nina", 100, 48, "gravel"),
    Bike(8, "Bike 3000", 1000, 50, "hybrid"),
    Bike(2, "Auberon", 2000, 52, "electronic")
    
    ]

'''
