"""Unit tests for user-related API routes.

This module contains tests for:
    - User registration with valid and invalid data.
    - User login with valid and invalid credentials.
    - Access to user-related routes with and without JWT authentication.

Test Cases:
    - TestUserAPI: Tests for user API endpoints.

Classes:
    - TestUserAPI: Unit tests for endpoints related to user registration, login, and retrieval.

Functions:
    - setUp: Initializes the Flask app and database for each test case.
    - tearDown: Cleans up the database after each test.
    - test_register_user: Verifies successful registration of a user with valid data.
    - test_register_user_invalid_phone: Ensures registration fails with an invalid phone number.
    - test_register_user_weak_password: Ensures registration fails with a weak password.
    - test_get_users_unprotected: Verifies access to user data is restricted without authentication.
    - test_login_user: Verifies successful login with valid credentials.
    - test_login_user_invalid_credentials: Ensures login fails with invalid credentials.
    - test_get_users_protected: Verifies user data can only be accessed with valid JWT authentication.
"""

import unittest

from app.entities.base import db
from app.entities.user import User, UserValidationError
from flask_jwt_extended import create_access_token

from app import create_app


class TestUserAPI(unittest.TestCase):
    """
    Unit tests for user-related API endpoints.
    """

    def setUp(self):
        """
        Set up the test application and database.
        """
        self.app = create_app(config_class="app.config.TestingConfigSimple")
        self.app.testing = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Tear down the test database.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        """
        Test user registration endpoint with valid data.
        """
        response = self.client.post(
            "/api/register_user/",
            json={
                "username": "testuser",
                "password": "Valid@1234",
                "email": "test@example.com",
                "phone_number": "+1234567890",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_register_user_invalid_phone(self):
        """
        Test user registration with invalid phone number.
        """
        response = self.client.post(
            "/api/register_user/",
            json={
                "username": "testuser",
                "password": "Valid@1234",
                "email": "test@example.com",
                "phone_number": "1234567890",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Phone number must start with a '+'", response.get_json().get("error")
        )

    def test_register_user_weak_password(self):
        """
        Test user registration with weak password.
        """
        response = self.client.post(
            "/api/register_user/",
            json={
                "username": "testuser",
                "password": "weakpass",
                "email": "test@example.com",
                "phone_number": "+1234567890",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Password must be at least 8 characters", response.get_json().get("error")
        )

    def test_get_users_unprotected(self):
        """
        Test retrieval of all users.
        """
        self.client.post(
            "/api/register_user/",
            json={
                "username": "testuser",
                "password": "Valid@1234",
                "email": "test@example.com",
                "phone_number": "+1234567890",
            },
        )
        response = self.client.get("/api/users/")
        # did not log in
        self.assertEqual(response.status_code, 401)

    def test_login_user_username(self):
        """
        Test user login endpoint with valid credentials.
        """
        self.client.post(
            "/api/register_user/",
            json={
                "username": "testuser",
                "password": "Valid@1234",
                "email": "test@example.com",
                "phone_number": "+1234567890",
            },
        )
        response = self.client.post(
            "/api/login_user/", json={"username": "testuser", "password": "Valid@1234"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("access_token", data)

    def test_login_user_email(self):
        """
        Test user login endpoint with valid credentials.
        """
        self.client.post(
            "/api/register_user/",
            json={
                "username": "testuser",
                "password": "Valid@1234",
                "email": "test@example.com",
                "phone_number": "+1234567890",
            },
        )
        response = self.client.post(
            "/api/login_user/",
            json={"username": "test@example.com", "password": "Valid@1234"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("access_token", data)

    def test_login_user_invalid_credentials(self):
        """
        Test user login endpoint with invalid credentials.
        """
        self.client.post(
            "/api/register_user/",
            json={
                "username": "testuser2",
                "password": "Valid@1234",
                "email": "test@example.com",
                "phone_number": "+1234567890",
            },
        )
        response = self.client.post(
            "/api/login_user/",
            json={"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 401)

    def test_get_users_protected(self):
        """
        Test retrieval of all users with JWT authentication.
        """
        with self.app.app_context():
            user = User(
                username="testuser",
                password="Valid@1234",
                email="test@example.com",
                phone_number="+1234567890",
            )
            db.session.add(user)
            db.session.commit()

            access_token = create_access_token(identity="testuser")

        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.get("/api/users/", headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["username"], "testuser")


if __name__ == "__main__":
    unittest.main()
