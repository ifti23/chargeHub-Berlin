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
from app.entities.charging_station import OperationStatus, ChargingType
from app.entities.postal_code import PostalCode


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

    @staticmethod
    def create_test_user():
        user = User(
            username="testuser",
            password="Valid@1234",
            email="test@example.com",
            phone_number="+1234567890",
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def generate_access_token(user):
        access_token = create_access_token(identity=user.username)
        return access_token

    @staticmethod
    def create_charging_station(functional=OperationStatus.OPERATIONAL):
        station = ChargingStation(
            functional=functional,
            postal_code_id=1,
            street="Test Street",
            house_number="42",
            latitude=52.52,
            longitude=13.405,
            operator="Test Operator",
            address_suffix="Near Park",
            nominal_power=50,
            charging_type=ChargingType.FAST,
            num_charging_points=4,
        )
        db.session.add(station)
        db.session.commit()
        return station

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
        with self.app.app_context():
            postal_data = (
                db.session.query(PostalCode)
                .filter_by(id=data[0]["postal_code_id"])
                .first()
            )
            self.assertEqual(postal_data.number, postal_code)

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
        Test updating the operational status of a charging station (requires login).
        """
        with self.app.app_context():
            user = self.create_test_user()
            access_token = self.generate_access_token(user)
            station = self.create_charging_station()

            # Test the update route with a new status
            headers = {"Authorization": f"Bearer {access_token}"}
            new_status = "used"
            response = self.client.post(
                f"/api/charging_stations/deactivate?station_id={station.id}&new_status={new_status}",
                headers=headers,
            )
            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertIn("message", data)
            self.assertIn(
                f"Charging station {station.id} updated to {new_status} successfully.",
                data["message"],
            )

    def test_deactivate_charging_station_invalid_status(self):
        """
        Test updating a charging station with an invalid status (requires login).
        """
        with self.app.app_context():
            user = self.create_test_user()
            access_token = self.generate_access_token(user)
            station = self.create_charging_station()

            # Test the update route with an invalid status
            headers = {"Authorization": f"Bearer {access_token}"}
            invalid_status = "invalid_status"
            response = self.client.post(
                f"/api/charging_stations/deactivate?station_id={station.id}&new_status={invalid_status}",
                headers=headers,
            )
            self.assertEqual(response.status_code, 400)
            data = response.get_json()
            self.assertIn("error", data)
            self.assertIn("Invalid status", data["error"])

    def test_deactivate_nonexistent_charging_station(self):
        """
        Test updating the operational status of a non-existent charging station.
        """
        with self.app.app_context():
            # Register a test user

            user = self.create_test_user()
            db.session.add(user)
            db.session.commit()

            # Generate a JWT token for the test user
            access_token = create_access_token(identity="testuser")

            # Test updating a non-existent station
            station_id = 9999
            headers = {"Authorization": f"Bearer {access_token}"}
            response = self.client.post(
                f"/api/charging_stations/deactivate?station_id={station_id}&new_status=operational",
                headers=headers,
            )
            self.assertEqual(response.status_code, 404)
            data = response.get_json()
            self.assertIn("error", data)
            self.assertIn("Charging station not found.", data["error"])

    def test_get_charging_stations_invalid_postal_code_format(self):
        """
        Test retrieving charging stations with a non-numeric postal code.
        """
        response = self.client.get("/api/charging_stations/postal_code/abcde")
        self.assertEqual(response.status_code, 404)  # Bad Request


if __name__ == "__main__":
    unittest.main()
