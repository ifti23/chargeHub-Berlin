import unittest

from app import create_app
from app.domain.entities.templates.base import db
from app.domain.entities.user import User
from app.domain.services.user_services.user_login_service import user_login_service
from flask_jwt_extended import decode_token
from werkzeug.exceptions import InternalServerError, Unauthorized


class TestUserLoginService(unittest.TestCase):
    """
    Integration tests for the `user_login_service` function.
    """

    def setUp(self):
        """
        Set up a test app and database for testing.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
        self.app.testing = True
        with self.app.app_context():
            db.create_all()
            # Add a test user with a hashed password
            self.test_user = User(
                username="test_user",
                email="test_user@example.com",
                password="test2_Password",
                phone_number="+1234567890",
            )
            db.session.add(self.test_user)
            db.session.commit()

    def tearDown(self):
        """
        Tear down the test database.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_successful_login(self):
        """
        Test successful login with valid credentials.
        """
        with self.app.app_context():
            # Call the login service with valid credentials
            token = user_login_service("test_user@example.com", "test2_Password")

            # Decode and verify the token
            decoded_token = decode_token(token)
            self.assertEqual(decoded_token["sub"], "test_user")

    def test_invalid_password(self):
        """
        Test login with an invalid password.
        """
        with self.app.app_context():
            with self.assertRaises(Unauthorized):
                user_login_service("test_user@example.com", "wrong_password")

    def test_user_not_found(self):
        """
        Test login with a non-existent user.
        """
        with self.app.app_context():
            with self.assertRaises(Unauthorized):
                user_login_service("nonexistent_user@example.com", "test_password")

    def test_database_error(self):
        """
        Test database error during login.
        """
        with self.app.app_context():
            # Simulate a database error by dropping the users table
            self.tearDown()

            with self.assertRaises(InternalServerError):
                user_login_service("test_user@example.com", "test_password")


if __name__ == "__main__":
    unittest.main()
