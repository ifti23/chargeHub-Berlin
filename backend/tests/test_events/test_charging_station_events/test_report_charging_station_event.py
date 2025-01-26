import unittest

from app import create_app
from app.domain.entities.charging_station import (
    ChargingStation,
    ChargingType,
    OperationStatus,
)
from app.domain.entities.templates.base import db


class TestReportChargingStationEvent(unittest.TestCase):
    """
    Integration tests for the `report_charging_station_event` endpoint.
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
            # Add a sample charging station
            station = ChargingStation(
                functional=OperationStatus.OPERATIONAL,
                postal_code_id=10115,
                street="Sample Street",
                house_number="123",
                latitude=52.5200,
                longitude=13.4050,
                operator="Operator A",
                charging_type=ChargingType.FAST,
                num_charging_points=4,
                nominal_power=50,
            )
            db.session.add(station)
            db.session.commit()

            self.station_id = station.id

    def tearDown(self):
        """
        Tear down the test database.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_successful_status_update(self):
        """
        Test successfully updating the status of a charging station.
        """
        response = self.client.post(
            "/api/charging_stations/change_status",
            query_string={"station_id": self.station_id, "new_status": "used"},
        )
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIn("message", data)

        # Verify the database is updated
        with self.app.app_context():
            updated_station = ChargingStation.query.get(self.station_id)
            self.assertEqual(updated_station.functional, OperationStatus.USED)

    def test_missing_station_id_or_new_status(self):
        """
        Test missing 'station_id' or 'new_status' parameters.
        """
        response = self.client.post(
            "/api/charging_stations/change_status",
            query_string={"station_id": self.station_id},  # Missing new_status
        )
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)

    def test_invalid_station_id_or_new_status(self):
        """
        Test invalid 'station_id' or 'new_status'.
        """
        response = self.client.post(
            "/api/charging_stations/change_status",
            query_string={"station_id": "invalid", "new_status": "unknown_status"},
        )
        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIn("error", data)

    def test_non_existent_station_id(self):
        """
        Test non-existent charging station ID.
        """
        response = self.client.post(
            "/api/charging_stations/change_status",
            query_string={"station_id": 99999, "new_status": "used"},
        )
        self.assertEqual(response.status_code, 404)

        data = response.get_json()
        self.assertIn("error", data)

    def test_internal_server_error(self):
        """
        Test internal server error during status update.
        """
        with self.app.app_context():
            # Simulate a database error by dropping the `charging_stations` table
            db.drop_all()

            response = self.client.post(
                "/api/charging_stations/change_status",
                query_string={"station_id": self.station_id, "new_status": "used"},
            )
            self.assertEqual(response.status_code, 500)

            data = response.get_json()
            self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
