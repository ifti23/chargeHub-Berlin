import unittest

from app import create_app
from app.domain.entities.templates.base import db
from app.domain.entities.user import User
from app.domain.services.user_services.user_register_service import (
    user_register_service,
)
from werkzeug.exceptions import BadRequest, InternalServerError


class TestUserRegisterService(unittest.TestCase):
    """
    Integration tests for the `user_register_service` function.
    """

    def setUp(self):
        """
        Set up a test app and database for testing.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
        self.app.testing = True
        with self.app.app_context():
            db.create_all()
            # Add a sample user to simulate a duplicate email case
            self.sample_user = User(
                username="existing_user",
                email="existing_user@example.com",
                password="Valid@1234",
            )
            db.session.add(self.sample_user)
            db.session.commit()

    def tearDown(self):
        """
        Tear down the test database.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_successful_registration(self):
        """
        Test successful registration with valid user data.
        """
        with self.app.app_context():
            user_data = {
                "username": "new_user",
                "email": "new_user@example.com",
                "password": "secure2%_Password",
                "phone_number": "+1234567890",
            }
            response = user_register_service(user_data)

            # Assertions
            self.assertIn("message", response)
            self.assertEqual(response["message"], "User registered successfully.")
            self.assertIn("user_id", response)
            self.assertIsInstance(response["user_id"], int)

            # Verify user is saved in the database
            user = User.query.filter_by(email="new_user@example.com").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "new_user")

    def test_missing_required_fields(self):
        """
        Test registration with missing required fields.
        """
        with self.app.app_context():
            # Missing email field
            incomplete_data = {
                "username": "incomplete_user",
                "password": "secure2%_Password",
            }
            with self.assertRaises(BadRequest):
                user_register_service(incomplete_data)

    def test_duplicate_email_registration(self):
        """
        Test registration with an email that already exists in the database.
        """
        with self.app.app_context():
            user_data = {
                "username": "new_user",
                "email": "existing_user@example.com",  # Duplicate email
                "password": "secure2%_Password",
                "phone_number": "+1234567890",
            }
            with self.assertRaises(BadRequest):
                user_register_service(user_data)

    def test_database_error(self):
        """
        Test registration when a database error occurs.
        """
        with self.app.app_context():
            user_data = {
                "username": "error_user",
                "email": "error_user@example.com",
                "password": "secure2%_Password",
                "phone_number": "+1234567890",
            }

            # Simulate a database error by temporarily dropping the users table
            db.drop_all()

            with self.assertRaises(InternalServerError):
                user_register_service(user_data)


if __name__ == "__main__":
    unittest.main()
