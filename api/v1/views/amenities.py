#!/usr/bin/python3
"""Handles API calls for Amenity objects"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, make_response, abort, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """GETs all amemities"""
    amenities = [amenity.to_dict() for amenity in
                 storage.all("Amenity").values()]
    return make_response(jsonify(amenities), 200)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """GETs amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return make_response(jsonify(amenity.to_dict()), 200)
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """DELETEs amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def add_amenity():
    """POSTs a new amenity"""
    if request.is_json:
        req = request.get_json()
        if "name" in req:
            amenity = Amenity(**req)
            amenity.save()
            return make_response(jsonify(amenity.to_dict()), 201)
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """UPDATEs an amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        if request.is_json:
            req = request.get_json()
            for k, v in req.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(amenity, k, v)
                amenity.save()
                return make_response(jsonify(amenity.to_dict()), 200)
        abort(400, "Not a JSON")
    abort(404)
