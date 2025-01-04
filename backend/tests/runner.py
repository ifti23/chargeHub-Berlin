"""Test runner for all unittests in the project.

This module is responsible for:
    - Manually loading all test modules from the project.
    - Combining the test cases into a unified test suite.
    - Running the test suite and displaying detailed results.

Features:
    - Executes test cases from entity and route test modules.
    - Provides a single entry point for running all tests in the project.
    - Returns appropriate exit codes for success or failure.

Test Modules Included:
    - test_entities.test_user
    - test_entities.test_postal_codes
    - test_entities.test_charging_station
    - test_routes.test_users
    - test_routes.test_charging_station
    - test_routes.test_postal_code

Functions:
    - run_all_tests: Loads, combines, and runs all test modules.

Usage:
    Run the script directly to execute all tests:
    ```bash
    python runner.py
    ```
"""

import sys
import unittest

import test_entities.test_charging_station as test_charging_station
import test_entities.test_postal_codes as test_postal_codes

# Test modules
import test_entities.test_user as test_user
import test_routes.test_charging_station as test_charging_station_routes
import test_routes.test_postal_code as test_postal_code_routes
import test_routes.test_users as test_user_routes


def run_all_tests():
    """
    Runs all test modules added
    """
    loader = unittest.TestLoader()

    # Create a test suite by manually adding all test classes
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromModule(test_user))
    suite.addTests(loader.loadTestsFromModule(test_postal_codes))
    suite.addTests(loader.loadTestsFromModule(test_charging_station))
    suite.addTests(loader.loadTestsFromModule(test_user_routes))
    suite.addTests(loader.loadTestsFromModule(test_charging_station_routes))
    suite.addTests(loader.loadTestsFromModule(test_postal_code_routes))

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with appropriate status code
    if not result.wasSuccessful():
        print("\nSome tests failed.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
