import unittest

from app import create_app
from app.domain.entities.charging_station import (
    ChargingStation,
    ChargingType,
    OperationStatus,
)
from app.domain.entities.postal_code import PostalCode
from app.domain.entities.templates.base import db


class TestChargingStationDB(unittest.TestCase):
    """
    Unit tests for ChargingStation model with database connection.
    """

    def setUp(self):
        self.app = create_app(config_class="app.config.TestingConfig")
        self.app.testing = True
        with self.app.app_context():
            db.create_all()
            # Add sample postal code
            self.postal_code_number = 10116
            postal_code = PostalCode(
                number=self.postal_code_number,
                polygon="POLYGON ((13.426850722330673 52.5447395629012, 13.427585122330674 52.5446708929012, 13.430167762330674 52.5436981729012))",
            )
            db.session.add(postal_code)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_charging_station_creation(self):
        """
        Test creation of a valid charging station.
        """
        with self.app.app_context():
            charging_station = ChargingStation(
                functional=OperationStatus.OPERATIONAL,
                postal_code_id=self.postal_code_number,
                street="Sample Street",
                house_number="123A",
                latitude=52.5200,
                longitude=13.4050,
                operator="Test Operator",
                address_suffix="Near Mall",
                nominal_power=50,
                charging_type=ChargingType.FAST,
                num_charging_points=4,
            )
            db.session.add(charging_station)
            db.session.commit()

            retrieved_station = ChargingStation.query.all()[-1]
            self.assertIsNotNone(retrieved_station)
            self.assertEqual(retrieved_station.functional, OperationStatus.OPERATIONAL)
            self.assertEqual(retrieved_station.postal_code_id, self.postal_code_number)
            self.assertEqual(retrieved_station.street, "Sample Street")
            self.assertEqual(retrieved_station.house_number, "123A")
            self.assertEqual(retrieved_station.latitude, 52.5200)
            self.assertEqual(retrieved_station.longitude, 13.4050)
            self.assertEqual(retrieved_station.operator, "Test Operator")
            self.assertEqual(retrieved_station.address_suffix, "Near Mall")
            self.assertEqual(retrieved_station.nominal_power, 50)
            self.assertEqual(retrieved_station.charging_type, ChargingType.FAST)
            self.assertEqual(retrieved_station.num_charging_points, 4)

    def test_charging_station_to_dict(self):
        """
        Test the `__dict__` method of ChargingStation.
        """
        with self.app.app_context():
            # Create and add a sample charging station
            charging_station = ChargingStation(
                functional=OperationStatus.OPERATIONAL,
                postal_code_id=self.postal_code_number,
                street="Sample Street",
                house_number="123A",
                latitude=52.5200,
                longitude=13.4050,
                operator="Test Operator",
                address_suffix="Near Mall",
                nominal_power=50,
                charging_type=ChargingType.FAST,
                num_charging_points=4,
            )
            db.session.add(charging_station)
            db.session.commit()

            # Retrieve the station and convert to dictionary
            retrieved_station = ChargingStation.query.all()[-1]
            station_dict = retrieved_station.get_dict()

            # Validate the dictionary representation
            self.assertEqual(station_dict["functional"], "operational")
            self.assertEqual(station_dict["postal_code_id"], self.postal_code_number)
            self.assertEqual(station_dict["street"], "Sample Street")
            self.assertEqual(station_dict["house_number"], "123A")
            self.assertEqual(station_dict["latitude"], 52.5200)
            self.assertEqual(station_dict["longitude"], 13.4050)
            self.assertEqual(station_dict["operator"], "Test Operator")
            self.assertEqual(station_dict["address_suffix"], "Near Mall")
            self.assertEqual(station_dict["nominal_power"], 50)
            self.assertEqual(station_dict["charging_type"], "fast")
            self.assertEqual(station_dict["num_charging_points"], 4)


if __name__ == "__main__":
    unittest.main()
