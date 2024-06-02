#!/usr/bin/python3
"""module for amenities routes
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.all_models import our_models
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'])
@swag_from('documentation/amenity/all_amenities.yml')
def get_amenities():
    """return json format for amenities object
    """
    amenities_list = []
    for item in storage.all(Amenity).values():
        amenities_list.append(item.to_dict())
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=['GET'])
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenities_id(amenity_id):
    """get json format for specific id
    """
    state = storage.get(Amenity, amenity_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'])
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenities_id(amenity_id):
    """delete state object based on id
    """
    state = storage.get(Amenity, amenity_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities/", methods=['POST'])
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
def post_amenities():
    """create new state object
    """
    if not request.get_json():
        abort(400, "Not a JSON")
        # raise NotFound(description="Missing name")
    # json_data = request.get_json()
    if 'name' not in request.get_json():
        abort(400, "Missing name")
        # raise NotFound(description="Missing name")
    state = Amenity(name=request.json['name'])
    # state = Amenity(name=json_data['name'])
    storage.new(state)
    storage.save()
    return (jsonify(state.to_dict())), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'])
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
def update_amenities(amenity_id):
    """create new name for state object
    """
    if not request.get_json():
        abort(400, "Not a JSON")
    # json_data = request.get_json()
    state = storage.get(Amenity, amenity_id)
    if state is None:
        abort(404)
    setattr(state, "name", request.json['name'])
    storage.save()
    return jsonify(state.to_dict()), 200
