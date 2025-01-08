"""User entity module.
Defines the User model

Classes:
    UserValidationError: Custom exception for user validation errors.
    User: Database model for application users.
"""

import re
from typing import Optional

from .base import BaseModel, db


class UserValidationError(Exception):
    """
    Custom exception for User validation errors.
    """

    pass


class User(BaseModel):
    """
    Database model for storing user data.

    Attributes:
        username (str): The user's username.
        password (str): The user's password.
        email (str): The user's email address.
        phone_number (str, optional): The user's phone number.
    """

    __tablename__ = "users"
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)

    def __init__(
        self,
        username: str,
        password: str,
        email: str,
        phone_number: Optional[str] = None,
    ):
        """
        Initialize a User instance.

        Args:
            username (str): The user's username.
            password (str): The user's password.
            email (str): The user's email address.
            phone_number (str, optional): The user's phone number.

        Raises:
            UserValidationError: If validation fails for any attribute.
        """
        if not username or not password or not email:
            raise UserValidationError("Username, password, and email are required.")
        if not self._is_valid_email(email):
            raise UserValidationError("Invalid email address.")
        if phone_number and not self._is_valid_phone_number(phone_number):
            raise UserValidationError("Phone number must start with a '+' sign.")
        if not self._is_strong_password(password):
            raise UserValidationError(
                "Password must be at least 8 characters long, contain a capital letter, a number, and a special character."
            )

        self.username = username
        self.password = password
        self.email = email
        self.phone_number = phone_number

    @staticmethod
    def _is_valid_email(email):
        """
        Validate the email format.

        Args:
            email (str): The email to validate.

        Returns:
            bool: True if email is valid, False otherwise.
        """
        return (
            re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
            is not None
        )

    @staticmethod
    def _is_valid_phone_number(phone_number):
        """
        Validate that the phone number starts with a '+' sign.

        Args:
            phone_number (str): The phone number to validate.

        Returns:
            bool: True if phone number is valid, False otherwise.
        """
        return phone_number.startswith("+")

    @staticmethod
    def _is_strong_password(password):
        """
        Validate that the password is strong.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if password is strong, False otherwise.
        """
        return (
            len(password) >= 8
            and any(char.isupper() for char in password)
            and any(char.isdigit() for char in password)
            and any(char in r"!@#$%^&*()-_=+[]{}|;:'\",.<>?/\\`~" for char in password)
        )
