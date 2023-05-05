#!/usr/bin/python3
"""Handles API calls for Amenities of a Place objects"""
from api.v1.views import app_views
from models import storage, storage_t
from flask import make_response, jsonify, abort, request


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """GET's a list of amenities of a place"""
    place = storage.get("Place", place_id)
    if place:
        amenities = []
        if storage_t == "db":
            amenities = place.amenities
        else:
            amenities = place.amenities()
        return jsonify(amenities)
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """DELETEs an amenity object"""
    place = storage.get("Place", id=place_id)
    amenity = storage.get("Amenity", id=amenity_id)
    if place and amenity:
        if storage_t == "db":
            amenities = place.amenities
        else:
            amenities = place.amenities()
        if amenity in amenities:
            if amenity:
                del amenities[amenity]
                place.save()
                return jsonify({})
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def add_amenity_to_place(place_id, amenity_id):
    """Adds a new Amenity of a place"""
    place = storage.get("Place", id=place_id)
    amenity = storage.get("Amenity", id=amenity_id)
    if place and amenity:
        if storage_t == "db":
            amenities = place.amenities
        else:
            amenities = place.amenities()
        if amenities:
            if amenity not in amenities:
                amenities.append(amenity)
                place.save()
                return make_response(jsonify(amenity.to_dict()), 201)
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
