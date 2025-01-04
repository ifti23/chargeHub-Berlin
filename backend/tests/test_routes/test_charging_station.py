"""
Unit tests for ChargingStation routes.

Test Cases:
    TestChargingStationRoutes: Tests for the ChargingStation API endpoints.
"""

import unittest

from app.entities.base import db
from app.entities.charging_station import ChargingStation
from app.entities.user import User
from flask_jwt_extended import create_access_token

from app import create_app


class TestChargingStationRoutes(unittest.TestCase):
    """
    Unit tests for ChargingStation API endpoints.
    """

    def setUp(self):
        """
        Set up the test application.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
        self.app.testing = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Tear down the test database.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_charging_stations(self):
        """
        Test retrieving all charging stations.
        """
        response = self.client.get("/api/charging_stations/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data), 0)
        self.assertIn("street", data[0])
        self.assertIn("house_number", data[0])

    def test_get_charging_stations_by_postal_code(self):
        """
        Test retrieving charging stations for a specific postal code.
        """
        postal_code = 10115  # Replace with a valid postal code from your dataset
        response = self.client.get(f"/api/charging_stations/postal_code/{postal_code}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]["postal_code_number"], postal_code)

    def test_get_charging_stations_by_invalid_postal_code(self):
        """
        Test retrieving charging stations with an invalid postal code.
        """
        response = self.client.get("/api/charging_stations/postal_code/99999")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("Postal code 99999 not found.", data["error"])

    def test_deactivate_charging_station(self):
        """
        Test deactivating a charging station (requires login).
        """
        with self.app.app_context():
            # Register a test user and create a charging station
            user = User(
                username="testuser",
                password="Valid@1234",
                email="test@example.com",
                phone_number="+1234567890",
            )
            db.session.add(user)
            db.session.commit()

            # Generate a JWT token for the test user
            access_token = create_access_token(identity="testuser")

            # Insert a sample charging station
            station_id = 10

            # Test the deactivate route
            headers = {"Authorization": f"Bearer {access_token}"}
            response = self.client.post(
                f"/api/charging_stations/{station_id}/deactivate", headers=headers
            )
            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertIn("message", data)
            self.assertIn(
                f"Charging station {station_id} deactivated successfully.",
                data["message"],
            )

            # Verify the station is now deactivated
            updated_station = ChargingStation.query.get(station_id)
            self.assertFalse(updated_station.functional)

    def test_deactivate_charging_station_not_logged_in(self):
        """
        Test deactivating a charging station without being logged in.
        """
        with self.app.app_context():
            station_id = 1  # Replace with a valid ID from your data

            response = self.client.post(
                f"/api/charging_stations/{station_id}/deactivate"
            )
            self.assertEqual(response.status_code, 401)  # Unauthorized


if __name__ == "__main__":
    unittest.main()
