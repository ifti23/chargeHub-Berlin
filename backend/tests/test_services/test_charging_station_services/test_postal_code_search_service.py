import unittest

from app import create_app
from app.domain.entities.templates.base import db
from app.domain.services.charging_staion_services.postal_code_search_service import (
    search_postal_code_service,
)
from werkzeug.exceptions import InternalServerError, NotFound


class TestSearchPostalCodeService(unittest.TestCase):
    """
    Integration tests for the `search_postal_code_service` function.
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

    def test_successful_search(self):
        """
        Test successful search for charging stations by postal code.
        """
        with self.app.app_context():
            response = search_postal_code_service("10115")

            # Assertions
            self.assertEqual(
                response["message"], "Successfully found charging stations."
            )
            self.assertGreater(len(response["stations"]), 2)

    def test_invalid_postal_code(self):
        """
        Test search with an invalid postal code.
        """
        with self.app.app_context():
            with self.assertRaises(NotFound):
                search_postal_code_service("99999")  # Non-existent postal code

            with self.assertRaises(NotFound):
                search_postal_code_service("invalid_code")  # Invalid format

    def test_database_error(self):
        """
        Test search when a database error occurs.
        """
        with self.app.app_context():
            # Simulate a database error by dropping the postal_codes table
            db.drop_all()

            with self.assertRaises(InternalServerError):
                search_postal_code_service("10115")


if __name__ == "__main__":
    unittest.main()
