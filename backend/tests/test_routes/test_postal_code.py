"""
Unit tests for PostalCode-related routes.

Test Cases:
    TestPostalCodeRoutes: Tests for PostalCode API endpoints.
"""

import csv
import os
import unittest

from app.entities.base import db
from app.entities.postal_code import PostalCode

from app import create_app


class TestPostalCodeRoutes(unittest.TestCase):
    """
    Unit tests for PostalCode API endpoints.
    """

    def setUp(self):
        """
        Set up the test application and database.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
        self.app.testing = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.postal_number = 10116
            self.postal_code = PostalCode(
                number=self.postal_number,
                polygon="POLYGON ((13.426850722330673 52.5447395629012, 13.427585122330674 52.5446708929012, 13.430167762330674 52.5436981729012))",
            )
            db.session.add(self.postal_code)
            db.session.commit()

    def tearDown(self):
        """
        Tear down the test database.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_postal_codes_all_exist(self):
        """
        Test retrieving all postal codes.
        """
        csv_file_path = os.path.abspath(self.app.config["POSTAL_CODE_CSV"])
        rows = 0
        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            next(reader, None)  # Skip the header row

            row_count = sum(1 for _ in reader)
        response = self.client.get("/api/postal_codes/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), row_count + 1)  # add another in setup

    def test_get_single_postal_code(self):
        response = self.client.get("/api/postal_codes/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        data.sort(key=lambda x: x["number"])
        self.assertEqual(data[1]["number"], self.postal_number)

    def test_get_postal_codes_db_error(self):
        """
        Test retrieving postal codes when a database error occurs.
        """
        self.tearDown()
        response = self.client.get("/api/postal_codes/")
        self.assertEqual(response.status_code, 500)
        self.assertIn("Database error", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
