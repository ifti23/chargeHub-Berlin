import unittest

from app import create_app
from app.domain.entities.templates.base import db
from app.infrastructure.database_operations.postal_code_operations import (
    PostalCodeOperations,
)


class TestPostalCodeOperations(unittest.TestCase):
    """
    Integration tests for the `PostalCodeOperations` class.
    """

    def setUp(self):
        """
        Set up a test app and database for testing.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
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

    def test_get_postal_code_details(self):
        """
        Test retrieving postal code details.
        """
        with self.app.app_context():
            with PostalCodeOperations() as repository:

                # Valid postal code
                details = repository.get_postal_code_details("10115")
                self.assertEqual(details["number"], 10115)

                # Non-existent postal code
                details = repository.get_postal_code_details("99999")
                self.assertEqual(details, {})

    def test_is_valid(self):
        """
        Test validating postal codes.
        """
        with self.app.app_context():
            with PostalCodeOperations() as repository:

                # Valid postal code in database
                self.assertTrue(repository.is_valid("10115"))

                # Valid postal code format but not in database
                self.assertFalse(repository.is_valid("99999"))

                # Invalid format (non-numeric)
                self.assertFalse(repository.is_valid("invalid_code"))

                # Empty postal code
                self.assertFalse(repository.is_valid(""))


if __name__ == "__main__":
    unittest.main()
