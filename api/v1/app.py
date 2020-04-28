#!/usr/bin/python3
"""
dddd
"""
from flask import Flask
from models import storage
from flask import jsonify
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.errorhandler(404)
def resource_not_found(error):
    return (jsonify(error="Not found"), 404)


@app.teardown_appcontext
def off_sesssion(_):
    """pending"""
    storage.close()

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host, port, threaded=True)
