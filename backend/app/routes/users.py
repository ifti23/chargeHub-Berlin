"""
User routes module.

This module defines API endpoints for managing user operations, including:
    - Retrieving all users (requires authentication).
    - Registering a new user.
    - Authenticating a user and providing a JWT token for session management.

Blueprints:
    - get_users: Blueprint for retrieving user information.
    - register_user: Blueprint for user registration.
    - login_user: Blueprint for user authentication.

Endpoints:
    - GET /api/users/: Retrieves a list of all registered users (requires authentication).
    - POST /api/register_user/: Registers a new user with the provided details.
    - POST /api/login_user/: Authenticates a user and returns a JWT token on success.

Functions:
    - users: Retrieves all users from the database and returns their details.
    - user_registration: Registers a new user with validation for input data.
    - user_login: Authenticates a user and provides a JWT token if credentials are valid.
"""

from app.entities.user import User, UserValidationError, db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required
from sqlalchemy.exc import SQLAlchemyError

get_users = Blueprint("get_users", __name__)
register_user = Blueprint("register_user", __name__)
login_user = Blueprint("login_user", __name__)


@get_users.route("/", methods=["GET"])
@jwt_required()  # Require login to access this route
def users():
    """Retrieve all users.

    Returns:
        JSON: A list of user details.

    Raises:
        401 Unauthorized: If the request lacks a valid JWT token.
    """
    found_users = User.query.all()
    return jsonify(
        [
            {
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
            }
            for user in found_users
        ]
    )


@register_user.route("/", methods=["POST"])
def user_registration():
    """Register a new user.

    Accepts:
        JSON: A dictionary containing:
            - username (str): The username of the user.
            - password (str): The password for the user.
            - email (str): The email address of the user.
            - phone_number (str, optional): The phone number of the user.

    Returns:
        JSON: A success message if the user is registered successfully.
        JSON: An error message with status 400 or 500 for validation or database errors.

    Raises:
        400 Bad Request: If the provided input data is invalid.
        500 Internal Server Error: If there is a database-related issue.
    """
    data = request.get_json()
    try:
        user = User(
            username=data["username"],
            password=data["password"],
            email=data["email"],
            phone_number=data.get("phone_number"),
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except UserValidationError as e:
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error: " + str(e)}), 500


@login_user.route("/", methods=["POST"])
def user_login():
    """
    Authenticate a user using either their username or email.

    Accepts:
        JSON: A dictionary containing:
            - username_or_email (str): The username or email of the user.
            - password (str): The password for the user.

    Returns:
        JSON: A JWT access token if authentication is successful.
        JSON: An error message with status 401 if authentication fails.

    Raises:
        401 Unauthorized: If the credentials are invalid.
    """
    data = request.get_json()
    user = User.query.filter(
        (User.username == data.get("username")) | (User.email == data.get("username"))
    ).first()

    if (
        user and user.password == data["password"]
    ):  # You should use a hashed password comparison
        # Generate a JWT access token
        access_token = create_access_token(identity=user.username)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"error": "Invalid credentials"}), 401
