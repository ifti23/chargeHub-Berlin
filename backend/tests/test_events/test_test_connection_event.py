import unittest

from app import create_app
from flask import Flask


class TestTestConnectionEvent(unittest.TestCase):
    """
    Tests for the `hello_world` event.
    """

    def setUp(self):
        """
        Set up a Flask test app.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
        self.client = self.app.test_client()

    def test_hello_world(self):
        """
        Test that the `/` endpoint returns the correct welcome message.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Welcome to the backend"})


if __name__ == "__main__":
    unittest.main()
