#!/usr/bin/python3
"""Handles API calls for Place_Review objects"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from flask import make_response, jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_place_reviews(place_id):
    """GET's a list of reviews"""
    place = storage.get("Place", place_id)
    if place:
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """"GET review"""
    review = storage.get("Review", id=review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """DELETEs a review object"""
    review = storage.get("Review", id=review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/places/<place_id>/reviews/", methods=["POST"],
                 strict_slashes=False)
def add_place_review(place_id):
    """Adds a new Review of a place"""
    place = storage.get("Place", id=place_id)
    if place:
        if request.is_json:
            req = request.get_json()
            user = storage.get("User", req.get("user_id", None))
            if user:
                # req["place_id"] = place_id
                set(req, "place_id", place_id)
                review = Review(**req)
                review.save()
                return make_response(jsonify(review.to_dict()), 201)
            else:
                abort(400, "Missing user_id")
        else:
            abort(400, "Not a JSON")
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """UPDATES a review object"""
    review = storage.get("Review", id=review_id)
    if review:
        if request.is_json:
            req = request.get_json()
            for k, v in req.items():
                if k not in ["id", "user_id", "created_at", "updated_at"]:
                    setattr(review, k, v)
            review.save()
            return make_response(jsonify(review.to_dict()), 200)
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
