#!/usr/bin/python3
"""api app declaration"""
from flask import Flask, make_response, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def teardown_session(exception=None):
    """Closes the db session"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """json 404 page"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or "0.0.0.0"
    port = getenv("HBNB_API_PORT") or "5000"

    app.run(host=host, port=port, threaded=True)
