import unittest

from app import create_app
from app.domain.entities.charging_station import (
    ChargingStation,
    ChargingType,
    OperationStatus,
)
from app.domain.entities.templates.base import db
from app.infrastructure.database_operations.charging_station_operations import (
    ChargingStationOperations,
)


class TestChargingStationOperations(unittest.TestCase):
    """
    Integration tests for the `ChargingStationOperations` class.
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

    def test_get_all_charging_stations(self):
        """
        Test retrieving all charging stations.
        """
        with self.app.app_context():
            with ChargingStationOperations() as repository:
                stations = repository.get_all_charging_stations()
                self.assertGreater(len(stations), 200)

    def test_get_charging_stations_by_postal_code(self):
        """
        Test retrieving charging stations by postal code.
        """
        with self.app.app_context():
            with ChargingStationOperations() as repository:

                # Retrieve by valid postal code
                stations = repository.get_charging_stations_by_postal_code(10115)
                self.assertGreater(len(stations), 2)

                # Retrieve by invalid postal code
                stations = repository.get_charging_stations_by_postal_code(99999)
                self.assertEqual(len(stations), 0)

                # Invalid type (should raise TypeError)
                with self.assertRaises(TypeError):
                    repository.get_charging_stations_by_postal_code(52.52)

                # Invalid value (should raise ValueError)
                with self.assertRaises(ValueError):
                    repository.get_charging_stations_by_postal_code("invalid_code")

    def test_update_charging_station_status(self):
        """
        Test updating the functional status of a charging station.
        """
        with self.app.app_context():
            with ChargingStationOperations() as repository:

                # Update status successfully
                station = db.session.query(ChargingStation).first()
                repository.update_charging_station_status(station, "used")
                station_updated = db.session.query(ChargingStation).first()
                self.assertEqual(str(station_updated.functional).upper(), "USED")


if __name__ == "__main__":
    unittest.main()
