"""User registration route.
    - Registering a new user.

Blueprints:
    - register_user: Blueprint for user registration.

Endpoints:
    - POST /api/register_user/: Registers a new user with the provided details..

Functions:
    - user_registration_event: Registers a new user with validation for input data.
"""

from app.domain.entities.user import UserValidationError
from app.domain.services.user_services.user_register_service import (
    user_register_service,
)
from flask import jsonify, request
from werkzeug.exceptions import BadRequest, InternalServerError

from . import register_user


@register_user.route("/", methods=["POST"])
def user_registration_event():
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
    try:
        # Extract data from the request
        data = request.get_json()

        if not data:
            raise BadRequest("Request must contain JSON data.")

        # Validate required fields
        required_fields = ["username", "email", "password"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise BadRequest(f"Missing fields: {', '.join(missing_fields)}")

        # Delegate the registration logic to the service
        result = user_register_service(data)

        return jsonify(result), 201

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except UserValidationError as e:
        return jsonify({"error": f"The provided e-mail already exists: {str(e)}"}), 400
    except InternalServerError as e:
        return jsonify({"error": str(e)}), 500
    except KeyError as e:
        return jsonify({"error": f"Missing key in request: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid value: {str(e)}"}), 400
