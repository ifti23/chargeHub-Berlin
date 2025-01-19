"""Unit tests for ChargingStation entity.

This module contains tests for:
    - Database operations and validations for the ChargingStation model.
    - Validation and creation of ChargingStation instances.

Test Cases:
    - TestChargingStationDB: Tests for ChargingStation model with database connection.
    - TestChargingStation: Tests for ChargingStation validation logic without database interaction.

Classes:
    - TestChargingStationDB: Tests that require database operations.
    - TestChargingStation: Tests for validation and instance creation of ChargingStation.

Functions:
    - setUp: Initializes the Flask app and database for tests requiring a database.
    - tearDown: Cleans up the database after each test.
    - test_charging_station_creation: Verifies creation of a valid ChargingStation with database.
    - test_invalid_latitude: Ensures invalid latitude raises a ValueError.
    - test_invalid_longitude: Ensures invalid longitude raises a ValueError.
"""

import unittest

from app.entities.base import db
from app.entities.charging_station import (
    ChargingStation,
    ChargingStationValidationError,
)
from app.entities.postal_code import PostalCode

from app import create_app


class TestChargingStationDB(unittest.TestCase):
    """
    Unit tests for ChargingStation model.
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
                functional=True,
                postal_code_id=self.postal_code_number,
                street="Sample Street",
                house_number="123A",
                latitude=52.5200,
                longitude=13.4050,
            )
            db.session.add(charging_station)
            db.session.commit()

            retrieved_station = ChargingStation.query.all()[-1]
            self.assertIsNotNone(retrieved_station)
            self.assertTrue(retrieved_station.functional)
            self.assertEqual(retrieved_station.postal_code_id, self.postal_code_number)
            self.assertEqual(retrieved_station.street, "Sample Street")
            self.assertEqual(retrieved_station.house_number, "123A")
            self.assertEqual(retrieved_station.latitude, 52.5200)
            self.assertEqual(retrieved_station.longitude, 13.4050)


class TestChargingStation(unittest.TestCase):

    def test_invalid_latitude(self):
        """
        Test creating a charging station with an invalid latitude.
        """
        with self.assertRaises(ChargingStationValidationError):
            ChargingStation(
                functional=True,
                postal_code_id=1,
                street="Sample Street",
                house_number="123A",
                latitude=100.0,  # Invalid latitude
                longitude=13.4050,
            )

    def test_invalid_longitude(self):
        """
        Test creating a charging station with an invalid longitude.
        """
        with self.assertRaises(ChargingStationValidationError):
            ChargingStation(
                functional=True,
                postal_code_id=1,
                street="Sample Street",
                house_number="123A",
                latitude=52.5200,
                longitude=200.0,  # Invalid longitude
            )


if __name__ == "__main__":
    unittest.main()
