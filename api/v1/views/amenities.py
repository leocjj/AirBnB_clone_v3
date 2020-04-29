#!/usr/bin/python3
"""
amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity(amenity_id=None):
    """
    Get
    """
    tmp_obj = []
    if not amenity_id:
        for val in storage.all(Amenity).values():
            tmp_obj.append(val.to_dict())
        return jsonify(tmp_obj)
    item = storage.get(Amenity, amenity_id)
    if item:
        return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """
    Delete
    """
    item = storage.get(Amenity, amenity_id)
    if item:
        storage.delete(item)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """
    Create
    """
    try:
        item_info = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if item_info:
        if "name" in item_info:
            item = Amenity(**item_info)
            item.save()
            return (jsonify(item.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id=None):
    """
    Update
    """
    item = storage.get(Amenity, amenity_id)
    if amenity_id and item:
        try:
            data = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if data:
            for k, v in data.items():
                if (k != "id" and k != "created_at" and k != "updated_at"):
                    setattr(item, k, v)

            item.save()
            return (jsonify(item.to_dict()))
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
