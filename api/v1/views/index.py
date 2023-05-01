#!/usr/bin/python3
"""index views"""
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """Status of api"""
    return make_response(jsonify({"status": "OK"}))


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Retrives number of objects by type"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    stats = {}
    for idn, cls in classes.items():
        stats[idn] = storage.count(cls)

    return make_response(jsonify(stats))
