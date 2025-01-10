"""Unit tests for PostalCode data and validation logic.

This module contains tests for:
    - Database initialization and data loading for PostalCode.
    - Validation and creation of PostalCode instances.

Test Cases:
    - TestPostalCodeDataDB: Tests that require the database, including data loading from CSV and matching database content.
    - TestPostalCodeData: Tests for PostalCode validation logic that do not require the database for faster execution.

Classes:
    - TestPostalCodeDataDB: Tests for database-related operations.
    - TestPostalCodeData: Tests for PostalCode validation and instance creation.

Functions:
    - setUp: Initializes the Flask app and database for tests requiring a database.
    - tearDown: Cleans up the database after each test.
    - test_postal_code_data_loaded: Verifies that data is loaded into the database during app initialization.
    - test_csv_data_matches_database: Validates that CSV file content matches the database.
    - test_valid_postal_code_creation: Tests creation of a valid PostalCode instance.
    - test_invalid_postal_code_number: Verifies that invalid postal code numbers raise errors.
    - test_invalid_polygon_format: Verifies that invalid polygon formats raise errors.
    - test_polygon_is_valid: Tests the validity of polygons using the static method.
"""

import csv
import os
import unittest

from app.entities.base import db
from app.entities.postal_code import PostalCode, PostalCodeValidationError

from app import create_app


class TestPostalCodeDataDB(unittest.TestCase):
    """
    Tests for PostalCode data initialization.
    """

    def setUp(self):
        self.app = create_app(config_class="app.config.TestingConfig")
        self.app.testing = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_postal_code_data_loaded(self):
        """
        Test that postal code data is loaded on app start.
        """
        with self.app.app_context():
            postal_codes = PostalCode.query.all()
            self.assertGreater(len(postal_codes), 0)

    def test_csv_data_matches_database(self):
        """
        Test that all entries from the CSV file are present in the database.
        """
        csv_file_path = os.path.abspath(self.app.config["POSTAL_CODE_CSV"])
        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            next(reader, None)  # Skip the header row
            csv_data = [(int(row[0]), row[1]) for row in reader]

        with self.app.app_context():
            db_data = [(pc.number, pc.polygon) for pc in PostalCode.query.all()]

        self.assertCountEqual(csv_data, db_data)


class TestPostalCodeData(unittest.TestCase):
    """The setup of the database takes too long. Create a seperate class for the tests that do not need the database"""

    def test_valid_postal_code_creation(self):
        """
        Test creating a valid PostalCode instance.
        """
        self._skip_setup = True
        postal_code = PostalCode(
            number=10405,
            polygon="POLYGON ((13.426850722330673 52.5447395629012, 13.427585122330674 52.5446708929012))",
        )
        self.assertEqual(postal_code.number, 10405)
        self.assertEqual(
            postal_code.polygon,
            "POLYGON ((13.426850722330673 52.5447395629012, 13.427585122330674 52.5446708929012))",
        )

    def test_invalid_postal_code_number(self):
        """
        Test creating a PostalCode with an invalid number.
        """
        self._skip_setup = True
        with self.assertRaises(PostalCodeValidationError):
            PostalCode(
                number=99999,
                polygon="POLYGON ((13.426850722330673 52.5447395629012, 13.427585122330674 52.5446708929012))",
            )

    def test_invalid_polygon_format(self):
        """
        Test creating a PostalCode with an invalid polygon format.
        """
        self._skip_setup = True
        with self.assertRaises(PostalCodeValidationError):
            PostalCode(number=10405, polygon="INVALID POLYGON FORMAT")

    def test_polygon_is_valid(self):
        """
        Test the polygon_is_valid static method.
        """
        self._skip_setup = True
        valid_polygon = "POLYGON ((13.426850722330673 52.5447395629012, 13.427585122330674 52.5446708929012))"
        invalid_polygon = "INVALID POLYGON FORMAT"
        self.assertTrue(PostalCode.polygon_is_valid(polygon=valid_polygon))
        self.assertFalse(PostalCode.polygon_is_valid(polygon=invalid_polygon))


if __name__ == "__main__":
    unittest.main()
