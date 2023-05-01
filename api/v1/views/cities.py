#!/usr/bin/python3
"""Handles API calls for City objects"""
from api.v1.views import app_views
from models import storage
from models.city import City
from flask import make_response, jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_state_cities(state_id):
    """GET's a list of cities"""
    state = storage.get("State", state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return make_response(jsonify(cities), 200)
    abort(404)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    """"GET city"""
    city = storage.get("City", id=city_id)
    if city:
        return make_response(jsonify(city.to_dict()), 200)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """DELETEs a city object"""
    city = storage.get("City", id=city_id)
    if city:
        city.delete()
        storage.save()
        return make_response(jsonify({}), 201)
    abort(404)


@app_views.route("/states/<state_id>/cities/", methods=["POST"],
                 strict_slashes=False)
def add_state_city(state_id):
    """Adds a new City of a state"""
    state = storage.get("State", id=state_id)
    if state:
        if request.is_json:
            req = request.get_json()
            if "name" in req:
                # req["state_id"] = state_id
                setattr(req, "state_id", state_id)
                city = City(**req)
                city.save()
                return make_response(jsonify(city.to_dict()), 201)
            abort(400, "Missing name")
        abort(400, "Not a JSON")
    abort(404)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """UPDATES a city object"""
    city = storage.get("City", id=city_id)
    if city:
        if request.is_json:
            req = request.get_json()
            for k, v in req.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(city, k, v)
            city.save()
            return make_response(jsonify(city.to_dict()), 200)
        abort(400, "Not a JSON")
    abort(404)
