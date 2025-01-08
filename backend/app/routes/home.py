"""
Hello route module.

Provides a simple endpoint to verify the application is running.
"""

from flask import Blueprint, jsonify

home = Blueprint("hello", __name__)


@home.route("/", methods=["GET"])
def hello_world():
    """
    Return a simple 'Hello, World!' message.

    Returns:
        JSON: A message indicating the application is running.
    """
    return jsonify({"message": "Welcome to the backend"}), 200
