"""User login event, called when a user tries to login
    - Authenticating a user and providing a JWT token for session management.

Blueprint:
    - login_user: Blueprint for user authentication.

Endpoints:
    - POST /api/login_user/: Authenticates a user and returns a JWT token on success.

Functions:
    - user_login_event: Authenticates a user and provides a JWT token if credentials are valid.
"""

from app.domain.services.user_services.user_login_service import user_login_service
from flask import jsonify, request
from werkzeug.exceptions import BadRequest, InternalServerError, Unauthorized

from . import login_user


@login_user.route("/", methods=["POST"])
def user_login_event():
    """
    Authenticate a user using either their username or email.

    Returns:
        JSON: A JWT access token if authentication is successful.
        JSON: An error message with status 401 if authentication fails.
    """
    try:
        data = request.get_json()

        if not data:
            raise BadRequest("Request data is missing.")

        username_or_email = data.get("username")
        password = data.get("password")

        if not username_or_email or not password:
            raise BadRequest("Both 'username' and 'password' are required.")

        # Delegate to the service layer
        access_token = user_login_service(username_or_email, password)
        return jsonify({"access_token": access_token}), 200

    except Unauthorized as e:
        return jsonify({"error": str(e)}), 401
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except InternalServerError as e:
        return jsonify({"error": str(e)}), 500
