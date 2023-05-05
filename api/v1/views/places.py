#!/usr/bin/python3
"""Handles API calls for Place objects"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from flask import jsonify, make_response, abort, request


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """Retrieves all place objects that are in a city"""
    city = storage.get("City", city_id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    else:
        abort(404)


@app_views.route("/places/<string:place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """
    Retrieves place by id
    Args:
        place_id (str): unique identifier
    """
    place = storage.get("Place", id=place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes place
    Args:
        place_id (str): Unique identifier
    """
    place = storage.get("Place", place_id)
    if place:
        place.delete()
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def add_city_place(city_id):
    """Adds a new city place"""
    city = storage.get("City", id=city_id)
    if city:
        if request.is_json:
            req = request.get_json()
            if "user_id" not in req:
                abort(400, "Missing user_id")
            # user = storage.get("User", id=req["user_id"])
            user = storage.get("User", id=req.get("user_id", None))
            if user:
                if "name" not in req:
                    abort(400, "Missing name")
                # req["city_id"] = city_id
                setattr(req, "city_id", city_id)
                place = Place(**req)
                place.save()
                return make_response(jsonify(place.to_dict()), 201)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates place
    Args:
        place_id (str): Unique id for place
    """
    place = storage.get("Place", place_id)
    if place:
        if request.is_json:
            req = request.get_json()
            for k, v in req.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(place, k, v)

            place.save()
            return jsonify(place.to_dict())
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)


@app_views.route("/places_search", methods=["POST"],
                 strict_slashes=False)
def get_x_places():
    """Retrieves places dependign on body request"""
    if request.is_json:
        req = request.get_json()
        states = req.get("states", [])
        cities = req.get("cities", [])
        places = []
        if req:
            for sid in states:
                _state = storage.get("State", sid)
                if _state:
                    for c in _state.cities:
                        if c not in cities:
                            cities.append(c.id)
            for cid in cities:
                _city = storage.get("City", cid)
                if _city:
                    places.append([p.to_dict() for p in _city.places])
            if "amenities" in req:
                if places:
                    _places = places
                else:
                    _places = storage.all("Place")
                for aid in req.get("amenities", []):
                    places = filter(lambda p: aid in p.amenities, _places)       
        else:
            places = [p.to_dict() for p in storage.all("Place")]
        return jsonify(places)
    else:
        abort(400, "Not a JSON")