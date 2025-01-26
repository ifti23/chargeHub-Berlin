import unittest

from app import create_app
from app.domain.entities.templates.base import db


class TestSearchPostalCodeEvent(unittest.TestCase):
    """
    Integration tests for the `search_postal_code_event` endpoint.
    """

    def setUp(self):
        """
        Set up a Flask test app and database for testing.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
        self.client = self.app.test_client()
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

    def test_successful_postal_code_search(self):
        """
        Test successful retrieval of charging stations by postal code.
        """
        response = self.client.get("/api/charging_stations/postal_code/10115")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn("message", data)
        self.assertIn("stations", data)
        self.assertGreater(len(data["stations"]), 10)

    def test_invalid_input_data(self):
        """
        Test retrieval with invalid postal code input.
        """
        response = self.client.get(
            "/api/charging_stations/postal_code/invalid_postal_code"
        )
        # this route does not exist
        self.assertEqual(response.status_code, 404)

    def test_postal_code_not_found(self):
        """
        Test retrieval with a non-existent postal code.
        """
        response = self.client.get("/api/charging_stations/postal_code/99999")
        self.assertEqual(response.status_code, 404)

        data = response.get_json()
        self.assertIn("error", data)

    def test_internal_server_error(self):
        """
        Test internal server error during retrieval.
        """
        with self.app.app_context():
            # Simulate a database error by dropping the postal_codes table
            db.drop_all()

            response = self.client.get("/api/charging_stations/postal_code/10115")
            self.assertEqual(response.status_code, 500)

            data = response.get_json()
            self.assertIn("error", data)
            self.assertEqual(data["error"], "An unexpected error occurred.")


if __name__ == "__main__":
    unittest.main()
