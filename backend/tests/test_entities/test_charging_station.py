import unittest
from app.entities.base import db
from app.entities.charging_station import (
    ChargingStation,
    ChargingStationValidationError,
    OperationStatus,
    ChargingType,
)
from app.entities.postal_code import PostalCode
from app import create_app


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


class TestChargingStation(unittest.TestCase):
    """
    Unit tests for ChargingStation validation logic.
    """

    def test_invalid_latitude(self):
        """Test creating a charging station with an invalid latitude."""
        with self.assertRaises(ChargingStationValidationError):
            ChargingStation(
                functional=OperationStatus.OPERATIONAL,
                postal_code_id=1,
                street="Sample Street",
                house_number="123A",
                latitude=100.0,  # Invalid latitude
                longitude=13.4050,
            )

    def test_invalid_longitude(self):
        """Test creating a charging station with an invalid longitude."""
        with self.assertRaises(ChargingStationValidationError):
            ChargingStation(
                functional=OperationStatus.OPERATIONAL,
                postal_code_id=1,
                street="Sample Street",
                house_number="123A",
                latitude=52.5200,
                longitude=200.0,  # Invalid longitude
            )

    def test_invalid_nominal_power(self):
        """Test creating a charging station with an invalid nominal power."""
        with self.assertRaises(ChargingStationValidationError):
            ChargingStation(
                functional=OperationStatus.OPERATIONAL,
                postal_code_id=1,
                street="Sample Street",
                house_number="123A",
                latitude=52.5200,
                longitude=13.4050,
                nominal_power=-10,  # Invalid nominal power
            )

    def test_invalid_num_charging_points(self):
        """Test creating a charging station with an invalid number of charging points."""
        with self.assertRaises(ChargingStationValidationError):
            ChargingStation(
                functional=OperationStatus.OPERATIONAL,
                postal_code_id=1,
                street="Sample Street",
                house_number="123A",
                latitude=52.5200,
                longitude=13.4050,
                num_charging_points=0,  # Invalid number of charging points
            )

    def test_invalid_charging_type(self):
        """Test creating a charging station with an invalid charging type."""
        with self.assertRaises(ChargingStationValidationError):
            ChargingStation(
                functional=OperationStatus.OPERATIONAL,
                postal_code_id=1,
                street="Sample Street",
                house_number="123A",
                latitude=52.5200,
                longitude=13.4050,
                charging_type="ultra-fast",  # Invalid charging type
            )

    def test_valid_charging_station(self):
        """Test creating a valid charging station without database."""
        station = ChargingStation(
            functional=OperationStatus.USED,
            postal_code_id=1,
            street="Sample Street",
            house_number="123A",
            latitude=52.5200,
            longitude=13.4050,
            operator="Valid Operator",
            address_suffix="Near Park",
            nominal_power=22,
            charging_type=ChargingType.NORMAL,
            num_charging_points=2,
        )
        self.assertEqual(station.functional, OperationStatus.USED)
        self.assertEqual(station.nominal_power, 22)
        self.assertEqual(station.charging_type, ChargingType.NORMAL)
        self.assertEqual(station.num_charging_points, 2)


if __name__ == "__main__":
    unittest.main()
