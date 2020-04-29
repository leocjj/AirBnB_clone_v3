#!/usr/bin/python3
"""
pending
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_city_by_state(state_id=None):
    """Get"""
    tmp_obj = []
    item = storage.get(State, state_id)
    if item:
        for val in item.cities:
            tmp_obj.append(val.to_dict())
        return jsonify(tmp_obj)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id=None):
    """Get"""
    item = storage.get(City, city_id)
    if item:
        return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """Delete"""
    item = storage.get(City, city_id)
    if item:
        storage.delete(item)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """Create"""

    item = storage.get(State, state_id)
    if not item:
        abort(404)

        for val in item.cities():
            tmp_obj.append(val.to_dict())
        return jsonify(tmp_obj)

    try:
        item_info = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if item_info:
        if "name" in item_info:
            item = City(**item_info)
            setattr(item, "state_id", state_id)
            item.save()
            return (jsonify(item.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


#@app_views.route("/states", methods=["PUT"], strict_slashes=False)
@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def put_city(city_id=None):
    """
    Update
    """
    item = storage.get(State, city_id)
    if item:
        try:
            data = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if data:
            for k, v in data.items():
                if (k != "id" and k != "city_id" and
                        k != "created_at" and k != "updated_at"):
                    setattr(item, k, v)
            item.save()
            return (jsonify(item.to_dict()))
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
