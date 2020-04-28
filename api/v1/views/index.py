#!/usr/bin/python3
"""
dddd
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status_ok():
    """
    pending
    """
    return jsonify(status="OK")
