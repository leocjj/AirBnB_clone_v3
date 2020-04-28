#!/usr/bin/python3
"""
Module to handle endpoints (routes)
that will return results from API.
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status_ok():
    """
    Return the status of the API:
    """
    return jsonify(status="OK")

@app_views.route("/stats")
def stats_quantity():
    """
    pending
    """
    names = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
        }
    data_count = {}
    for k, name in names.items():
        data_count[name] = storage.count(k)
    return jsonify(data_count)
