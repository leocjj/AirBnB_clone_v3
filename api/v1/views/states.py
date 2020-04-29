#!/usr/bin/python3
"""
pending
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False)
@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id=None):
    """
    Get
    """
    tmp_obj = []
    if not state_id:
        for val in storage.all(State).values():
            tmp_obj.append(val.to_dict())
        return jsonify(tmp_obj)
    item = storage.get(State, state_id)
    if item:
        return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """
    Delete
    """
    item = storage.get(State, state_id)
    if item:
        storage.delete(item)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def post_state():
    """
    Create
    """
    try:
        item_info = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if item_info:
        if "name" in item_info:
            item = State(**item_info)
            item.save()
            return (jsonify(item.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/states", methods=["PUT"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def put_state(state_id=None):
    """
    Update
    """
    item = storage.get(State, state_id)
    if state_id and item:
        try:
            data = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if data:
            for k, v in data.items():
                if (k != "id" and k != "state_id" and
                        k != "created_at" and k != "updated_at"):
                    setattr(item, k, v)

            item.save()
            return (jsonify(item.to_dict()))
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
