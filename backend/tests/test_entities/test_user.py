"""
Unit tests for the User class.

Test Cases:
    TestUserClass: Tests for User model and validation logic.
"""

import unittest

from app.entities.base import db
from app.entities.user import User, UserValidationError

from app import create_app


class TestUserClass(unittest.TestCase):
    """
    Unit tests for the User class.
    """

    def setUp(self):
        """
        Set up the test application and database.
        """
        self.app = create_app(
            config_class="app.config.TestingConfigSimple"
        )  # not initializing the data saves a lot of time
        self.app.testing = True
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Tear down the test database.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_valid_user_creation(self):
        """
        Test creating a valid user instance.
        """
        user = User(
            username="testuser",
            password="Valid@1234",
            email="test@example.com",
            phone_number="+1234567890",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.phone_number, "+1234567890")

    def test_invalid_email(self):
        """
        Test user creation with an invalid email format.
        """
        with self.assertRaises(UserValidationError):
            User(
                username="testuser",
                password="Valid@1234",
                email="invalidemail",
                phone_number="+1234567890",
            )

    def test_invalid_phone_number(self):
        """
        Test user creation with an invalid phone number.
        """
        with self.assertRaises(UserValidationError):
            User(
                username="testuser",
                password="Valid@1234",
                email="test@example.com",
                phone_number="1234567890",
            )

    def test_weak_password_no_special_char(self):
        """
        Test user creation with a weak password (missing special character).
        """
        with self.assertRaises(UserValidationError):
            User(
                username="testuser",
                password="WeakPass1",
                email="test@example.com",
                phone_number="+1234567890",
            )

    def test_weak_password_no_uppercase(self):
        """
        Test user creation with a weak password (missing uppercase letter).
        """
        with self.assertRaises(UserValidationError):
            User(
                username="testuser",
                password="valid@1234",
                email="test@example.com",
                phone_number="+1234567890",
            )

    def test_weak_password_too_short(self):
        """
        Test user creation with a weak password (too short).
        """
        with self.assertRaises(UserValidationError):
            User(
                username="testuser",
                password="V@1",
                email="test@example.com",
                phone_number="+1234567890",
            )

    def test_missing_required_fields(self):
        """
        Test user creation with missing required fields.
        """
        with self.assertRaises(UserValidationError):
            User(username="", password="Valid@1234", email="test@example.com")

        with self.assertRaises(UserValidationError):
            User(username="testuser", password="", email="test@example.com")

        with self.assertRaises(UserValidationError):
            User(username="testuser", password="Valid@1234", email="")

    def test_user_database_insertion(self):
        """
        Test inserting a user into the database.
        """
        with self.app.app_context():
            user = User(
                username="dbuser",
                password="Secure@1234",
                email="dbuser@example.com",
                phone_number="+1234567890",
            )
            db.session.add(user)
            db.session.commit()

            retrieved_user = User.query.filter_by(username="dbuser").first()
            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.username, "dbuser")
            self.assertEqual(retrieved_user.email, "dbuser@example.com")
            self.assertEqual(retrieved_user.phone_number, "+1234567890")


if __name__ == "__main__":
    unittest.main()
