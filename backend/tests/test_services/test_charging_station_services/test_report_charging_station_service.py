import unittest

from app import create_app
from app.domain.entities.charging_station import (
    ChargingStation,
    ChargingType,
    OperationStatus,
)
from app.domain.entities.templates.base import db
from app.domain.services.charging_staion_services.report_charging_station_service import (
    change_charging_station_status,
)
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound


class TestChangeChargingStationStatus(unittest.TestCase):
    """
    Integration tests for the `change_charging_station_status` service function.
    """

    def setUp(self):
        """
        Set up a test app and database for testing.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
        self.app.testing = True
        with self.app.app_context():
            db.create_all()
            # Add a sample charging station
            station = ChargingStation(
                functional=OperationStatus.OPERATIONAL,
                postal_code_id=10116,
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
        Test successful update of charging station status.
        """
        with self.app.app_context():
            response = change_charging_station_status(self.station_id, "USED")

            # Assertions
            self.assertIn("Success", response["message"])

            # Verify the update in the database
            updated_station = ChargingStation.query.get(self.station_id)
            self.assertEqual(updated_station.functional, OperationStatus.USED)

    def test_invalid_status(self):
        """
        Test update with an invalid status.
        """
        with self.app.app_context():
            with self.assertRaises(BadRequest):
                change_charging_station_status(self.station_id, "INVALID_STATUS")

    def test_non_existent_station(self):
        """
        Test update for a non-existent charging station.
        """
        with self.app.app_context():
            with self.assertRaises(NotFound):
                change_charging_station_status(9999, "USED")  # Non-existent station ID

    def test_database_error(self):
        """
        Test database error during status update.
        """
        with self.app.app_context():
            # Simulate a database error by dropping the charging_stations table
            db.drop_all()

            with self.assertRaises(InternalServerError):
                change_charging_station_status(self.station_id, "USED")


if __name__ == "__main__":
    unittest.main()
