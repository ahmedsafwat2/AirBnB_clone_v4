#!/usr/bin/python3
"""module for places routes
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.all_models import our_models
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route('/cities/<city_id>/places/', methods=['GET'])
@app_views.route('/cities/<city_id>/places', methods=['GET'])
@swag_from('documentation/place/get_places.yml', methods=['GET'])
def get_places(city_id):
    """return json format for places object
    """
    places_list = []
    for item in storage.all(Place).values():
        dict_item = item.to_dict()
        if dict_item['city_id'] == city_id:
            places_list.append(dict_item)
    if places_list == []:
        abort(404)
    return jsonify(places_list)


@app_views.route("/places/<place_id>/", methods=['GET'])
@app_views.route("/places/<place_id>", methods=['GET'])
def get_places_id(place_id):
    """get json format for specific id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>/", methods=['DELETE'])
@app_views.route("/places/<place_id>", methods=['DELETE'])
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_places_id(place_id):
    """delete city object based on id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places/", methods=['POST'])
@app_views.route("/cities/<city_id>/places", methods=['POST'])
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def post_places(city_id):
    """create new place object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing user_id")
    if 'user_id' not in request.get_json():
        abort(400, "Missing name")

    place = Place(
        name=request.json['name'], city_id=city_id,
        user_id=request.json['user_id'])
    storage.new(place)
    storage.save()
    return (jsonify(place.to_dict())), 201


@app_views.route("/places/<place_id>/", methods=['PUT'])
@app_views.route("/places/<place_id>", methods=['PUT'])
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def update_places(place_id):
    """create new name for place object
    """
    args = ["name", "description", "number_rooms",
            "number_bathrooms", "max_guest",
            "price_by_night", "latitude",
            "longitude", "amenity_ids"]
    if not request.get_json():
        abort(400, "Not a JSON")
    # json_data = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for attr in args:
        if attr in request.get_json():
            setattr(place, attr, request.json[attr])
    storage.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/place/post_search.yml', methods=['POST'])
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)

