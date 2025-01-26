import unittest

from app import create_app
from app.domain.entities.templates.base import db
from app.domain.entities.user import User, UserValidationError
from app.infrastructure.database_operations.user_operations import UserOperations


class TestUserOperations(unittest.TestCase):
    """
    Integration tests for the `UserOperations` class.
    """

    def setUp(self):
        """
        Set up a test app and database for testing.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
        self.app.testing = True
        with self.app.app_context():
            db.create_all()
            # Add a sample user
            self.sample_user = User(
                username="test_user",
                email="test_user@example.com",
                password="test2_Password",
                phone_number="+1234567890",
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

    def test_get_user_by_username_or_email(self):
        """
        Test retrieving a user by username or email.
        """
        with self.app.app_context():
            with UserOperations() as repository:

                # Retrieve by username
                user = repository.get_user_by_username_or_email("test_user")
                self.assertIsNotNone(user)
                self.assertEqual(user.username, "test_user")

                # Retrieve by email
                user = repository.get_user_by_username_or_email("test_user@example.com")
                self.assertIsNotNone(user)
                self.assertEqual(user.email, "test_user@example.com")

                # Retrieve non-existent user
                user = repository.get_user_by_username_or_email("nonexistent_user")
                self.assertIsNone(user)

    def test_user_exists(self):
        """
        Test checking if a user exists by email or username.
        """
        with self.app.app_context():
            with UserOperations() as repository:

                # Check existing user by email
                exists = repository.user_exists(
                    email="test_user@example.com", username="nonexistent_user"
                )
                self.assertTrue(exists)

                # Check existing user by username
                exists = repository.user_exists(
                    email="nonexistent_email@example.com", username="test_user"
                )
                self.assertTrue(exists)

                # Check non-existent user
                exists = repository.user_exists(
                    email="nonexistent_email@example.com", username="nonexistent_user"
                )
                self.assertFalse(exists)

    def test_add_user(self):
        """
        Test adding a new user to the database.
        """
        with self.app.app_context():
            with UserOperations() as repository:

                # Add a new user
                new_user_data = {
                    "username": "new_user",
                    "email": "new_user@example.com",
                    "password": "secure123_Password",
                    "phone_number": "+0987654321",
                }
                new_user_id = repository.add_user(new_user_data)
                self.assertIsNotNone(new_user_id)

                # Verify the user exists in the database
                user = repository.get_user_by_username_or_email("new_user")
                self.assertIsNotNone(user)
                self.assertEqual(user.username, "new_user")

                # Attempt to add a user with duplicate email or username
                with self.assertRaises(UserValidationError):
                    repository.add_user(new_user_data)


if __name__ == "__main__":
    unittest.main()
