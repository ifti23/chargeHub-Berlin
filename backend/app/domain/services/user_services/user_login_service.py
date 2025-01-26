"""This module provides the user authentication service.

The `user_login_service` function handles user authentication by validating
credentials and generating JWT access tokens.
"""

from app.infrastructure.database_operations.user_operations import UserOperations
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, Unauthorized


def user_login_service(username_or_email: str, password: str) -> str:
    """
    Authenticate the user by username or email and password.

    This function retrieves the user from the database using the provided
    username or email and validates the password. If authentication is
    successful, it generates a JWT access token.

    Args:
        username_or_email (str): The username or email of the user.
        password (str): The password provided by the user.

    Returns:
        str: A JWT access token if authentication is successful.

    Raises:
        Unauthorized: If the user does not exist or the password is incorrect.
        InternalServerError: If a database error occurs during user retrieval.
    """
    try:
        with UserOperations() as repository:
            user = repository.get_user_by_username_or_email(username_or_email)

            if not user or user.password != password:
                raise Unauthorized("Invalid credentials")

    except SQLAlchemyError as e:
        raise InternalServerError(f"Database error: {str(e)}")

    # Generate and return a JWT access token
    return create_access_token(identity=user.username)
