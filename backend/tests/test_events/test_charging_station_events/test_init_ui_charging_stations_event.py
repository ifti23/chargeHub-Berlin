import unittest

from app import create_app
from app.domain.entities.templates.base import db


class TestInitUIChargingStationsEvent(unittest.TestCase):
    """
    Integration tests for the `init_ui_charging_stations_event` endpoint.
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

    def test_successful_retrieval(self):
        """
        Test successful retrieval of charging stations.
        """
        response = self.client.get("/api/charging_stations/")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertIn("message", data)
        self.assertIn("stations", data)
        self.assertGreater(len(data["stations"]), 250)

    def test_internal_server_error(self):
        """
        Test internal server error during charging stations retrieval.
        """
        with self.app.app_context():
            # Simulate a database error by dropping the `charging_stations` table
            db.drop_all()

            response = self.client.get("/api/charging_stations/")
            self.assertEqual(response.status_code, 500)

            data = response.get_json()
            self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
