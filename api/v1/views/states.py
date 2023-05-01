#!/usr/bin/python3
"""Handles API calls for State objects"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, make_response, abort, request


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves all state objects"""
    states = [state.to_dict() for state in storage.all("State").values()]
    return make_response(jsonify(states), 200)


@app_views.route("/states/<string:state_id>", methods=["GET"],
                 strict_slashes=False)
def get_state(state_id):
    """
    Retrieves state by id
    Args:
        state_id (str): unique identifier
    """
    state = storage.get("State", id=state_id)
    if state is None:
        abort(404)
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes state
    Args:
        state_id (str): Unique identifier
    """
    state = storage.get("State", state_id)
    if state:
        state.delete()
        storage.save()    
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def add_state():
    """Adds a new state"""
    if request.is_json:
        req = request.get_json()
        if "name" in req:
            state = State(**req)
            state.save()
            return make_response(jsonify(state.to_dict()), 201)
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Updates state
    Args:
        state_id (str): Unique id for state
    """
    state = storage.get("State", state_id)
    if state:
        if request.is_json:
            req = request.get_json()
            for k, v in req.items():
                if k not in ["id", "created_at", "updated_at"]:
                    setattr(state, k, v)

            state.save()
            return make_response(jsonify(state.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
