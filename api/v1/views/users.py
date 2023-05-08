#!/usr/bin/python3
"""Handles API calls for User objects"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, make_response, abort, request


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves all user objects"""
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route("/users/<string:user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """
    Retrieves user by id
    Args:
        user_id (str): unique identifier
    """
    user = storage.get("User", id=user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes user
    Args:
        user_id (str): Unique identifier
    """
    user = storage.get("User", user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def add_user():
    """Adds a new User"""
    if request.is_json:
        req = request.get_json()
        if "email" not in req:
            abort(400, "Missing email")
        elif "password" not in req:
            abort(400, "Missing, password")
        else:
            user = User(**req)
            user.save()
            return make_response(jsonify(user.to_dict()), 201)
    else:
        abort(400, "Not a JSON")


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Updates user
    Args:
        user_id (str): Unique id for user
    """
    user = storage.get("User", user_id)
    if user:
        if request.is_json:
            req = request.get_json()
            for k, v in req.items():
                if k not in ["id", "email", "created_at", "updated_at"]:
                    setattr(user, k, v)

            user.save()
            return jsonify(user.to_dict())
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
