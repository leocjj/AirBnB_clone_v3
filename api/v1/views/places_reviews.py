#!/usr/bin/python3
"""
places_review module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_review_by_state(place_id=None):
    """Get"""
    tmp_obj = []
    item = storage.get(Place, place_id)
    if item:
        for val in item.reviews:
            tmp_obj.append(val.to_dict())
        return jsonify(tmp_obj)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id=None):
    """Get"""
    item = storage.get(Review, review_id)
    if item:
        return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Delete"""
    item = storage.get(Review, review_id)
    if item:
        storage.delete(item)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """Create"""

    item = storage.get(Place, place_id)
    if not item:
        abort(404)

    try:
        item_info = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if item_info:
        if 'user_id' not in item_info:
            abort(400, "Missing user_id")
        u = storage.get(User, item_info["user_id"])
        if not u:
            abort(404)
        if 'text' not in item_info:
            abort(400, "Missing text")
        item = Review(**item_info)
        setattr(item, "place_id", place_id)
        item.save()
        return (jsonify(item.to_dict()), 201)
    
    else:
        abort(400, "Not a JSON")


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def put_review(review_id=None):
    """
    Update
    """
    item = storage.get(Review, review_id)
    if item:
        try:
            item_info = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if item_info:
            for k, v in item_info.items():
                if (k != "id" and k != "place_id" and
                        k != "user_id" and
                        k != "created_at" and k != "updated_at"):
                    setattr(item, k, v)
            item.save()
            return (jsonify(item.to_dict()))
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
