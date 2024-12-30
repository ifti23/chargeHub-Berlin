from flask import Blueprint, jsonify

home_message = Blueprint("home_message", __name__)


# Home route
@home_message.route("/")
def home():
    """Home message"""
    return jsonify({"message": "Welcome to the modularized Flask API!"})
