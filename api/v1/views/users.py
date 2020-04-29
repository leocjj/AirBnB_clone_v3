#!/usr/bin/python3
"""
user module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users", strict_slashes=False)
@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id=None):
    """
    Get
    """
    tmp_obj = []
    if not user_id:
        for val in storage.all(User).values():
            tmp_obj.append(val.to_dict())
        return jsonify(tmp_obj)
    item = storage.get(User, user_id)
    if item:
        return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """
    Delete
    """
    item = storage.get(User, user_id)
    if item:
        storage.delete(item)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def post_user():
    """
    Create
    """
    try:
        item_info = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if item_info:
        if "email" in item_info and "password" in item_info:
            item = User(**item_info)
            item.save()
            return (jsonify(item.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id=None):
    """
    Update
    """
    item = storage.get(User, user_id)
    if user_id and item:
        try:
            item_info = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if item_info:
            for k, v in item_info.items():
                if (k != "id" and k != "created_at" and
                        k != "email" and k != "updated_at"):
                    setattr(item, k, v)

            item.save()
            return (jsonify(item.to_dict()))
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
