from flask import Blueprint, jsonify

get_users = Blueprint("get_users", __name__)


@get_users.route("/", methods=["GET"])
def users():
    """Get all registered users"""
    return jsonify({"message": "Some Users"})
