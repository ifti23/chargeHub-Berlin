from app.infrastructure.database_operations.user_operations import UserOperations
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, InternalServerError


def user_register_service(user_data: dict) -> dict:
    """Validate and register a new user.

    Args:
        user_data (dict): Dictionary containing `username`, `email`, `password`, and optionally `phone_number`.

    Returns:
        dict: A confirmation message with the registered user's ID.

    Raises:
        BadRequest: If validation fails or user already exists.
    """
    try:
        username = user_data["username"]
        email = user_data["email"]
        password = user_data["password"]
        # the get method does not raise a keyerror
        phone_number = user_data.get("phone_number")

    except KeyError:
        # If called through the api route, this should never occur
        raise BadRequest("The fields (username, email, password) are required.")

    # Extract optional fields
    try:
        with UserOperations() as repository:

            if repository.user_exists(username=username, email=email):
                raise BadRequest("A user with this email already exists.")

            # Prepare user data for saving
            user_data_to_save = {
                "username": username,
                "email": email,
                "password": password,
                "phone_number": phone_number,
            }

            # Save the new user to the database
            user_id = repository.add_user(user_data_to_save)
    except SQLAlchemyError as e:
        raise InternalServerError(f"Database Error: {str(e)}")

    return {"message": "User registered successfully.", "user_id": user_id}
