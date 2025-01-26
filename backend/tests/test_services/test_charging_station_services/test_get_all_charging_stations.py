import unittest

from app import create_app
from app.domain.entities.charging_station import (
    ChargingStation,
    ChargingType,
    OperationStatus,
)
from app.domain.entities.templates.base import db
from app.domain.services.charging_staion_services.charging_stations_get_all_service import (
    get_all_charging_stations,
)
from werkzeug.exceptions import InternalServerError


class TestGetAllChargingStationsService(unittest.TestCase):
    """
    Integration tests for the `get_all_charging_stations` service function.
    """

    def setUp(self):
        """
        Set up a test app and database for testing.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
        self.app.testing = True
        with self.app.app_context():
            db.create_all()
            # Add sample charging stations
            self.station1 = ChargingStation(
                functional=OperationStatus.OPERATIONAL,
                postal_code_id=10115,
                street="Sample Street 1",
                house_number="123",
                latitude=52.5200,
                longitude=13.4050,
                operator="Operator A",
                charging_type=ChargingType.FAST,
                num_charging_points=4,
                nominal_power=50,
            )
            self.station2 = ChargingStation(
                functional=OperationStatus.MALFUNCTIONING,
                postal_code_id=10115,
                street="Sample Street 2",
                house_number="456",
                latitude=52.5205,
                longitude=13.4055,
                operator="Operator B",
                charging_type=ChargingType.NORMAL,
                num_charging_points=2,
                nominal_power=50,
            )
            db.session.add_all([self.station1, self.station2])
            db.session.commit()

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
        with self.app.app_context():
            response = get_all_charging_stations()

            # Assertions
            self.assertEqual(
                response["message"], "Successfully found charging stations."
            )
            self.assertGreater(len(response["stations"]), 250)

    def test_database_error(self):
        """
        Test database error during charging station retrieval.
        """
        with self.app.app_context():
            # Simulate a database error by temporarily dropping the charging_stations table
            db.drop_all()

            with self.assertRaises(InternalServerError):
                get_all_charging_stations()


if __name__ == "__main__":
    unittest.main()
