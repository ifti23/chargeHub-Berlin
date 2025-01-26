import unittest

from app import create_app
from app.domain.entities.templates.base import db
from app.domain.entities.user import User
from flask_jwt_extended import decode_token


class TestUserLoginEvent(unittest.TestCase):
    """
    Integration tests for the `user_login_event` endpoint.
    """

    def setUp(self):
        """
        Set up a Flask test app and database for testing.
        """
        self.app = create_app(config_class="app.config.TestingConfig")
        self.client = self.app.test_client()
        self.app.testing = True

        with self.app.app_context():
            db.create_all()
            # Add a sample user with a hashed password
            self.test_user = User(
                username="test_user2",
                email="test_user@example.com",
                password="valid%2_Password",
            )
            db.session.add(self.test_user)
            db.session.commit()

    def tearDown(self):
        """
        Tear down the test database.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_successful_login(self):
        """
        Test successful login with valid credentials.
        """
        response = self.client.post(
            "/api/login_user/",
            json={
                "username": "test_user@example.com",
                "password": "valid%2_Password",
            },
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("access_token", data)

    def test_missing_request_data(self):
        """
        Test login with missing request data.
        """
        response = self.client.post("/api/login_user/", json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_missing_username_or_password(self):
        """
        Test login with missing username or password.
        """
        response = self.client.post(
            "/api/login_user/",
            json={"username": "test_user@example.com"},  # Missing password
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_invalid_credentials(self):
        """
        Test login with invalid credentials.
        """
        response = self.client.post(
            "/api/login_user/",
            json={
                "username": "test_user@example.com",
                "password": "wrong_password",
            },
        )
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
