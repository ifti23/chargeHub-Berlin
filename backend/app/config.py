"""Configuration file for the REST API.

This module defines configurations for different environments, including:
    - Base configuration for common attributes.
    - Environment-specific configurations for development, testing, and production.

Classes:
    - Config: Base configuration class for all environments.
    - TestingConfig: Configuration for running unit tests with in-memory database and data initialization.
    - TestingConfigSimple: Lightweight testing configuration without data initialization.
    - (Optional) DevelopmentConfig: Configuration for local development.
    - (Optional) ProductionConfig: Configuration for production deployment.

Attributes:
    - DEBUG (bool): Enables or disables debug mode.
    - CHARGING_STATION_CSV (str): Path to the `Ladesaeulenregister.csv` file.
    - INIT_DATA (bool): Flag to determine if initial data should be loaded into the database.
    - JWT_SECRET_KEY (str): Secret key for JWT-based session management.
    - POSTAL_CODE_CSV (str): Path to the `geodata_berlin_plz.csv` file.
    - SERVER_PORT (int): The port on which the server listens for requests.
    - SQLALCHEMY_DATABASE_URI (str): Database URI for the application.
    - SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disables SQLAlchemy event system to improve performance.
    - TESTING (bool): Indicates if the application is running in a testing environment.

Usage:
    Import the appropriate configuration class into the application factory function:
    ```python
    from config import Config, TestingConfig, TestingConfigSimple
    ```

To set in development:
    - Customize the `DevelopmentConfig` and `ProductionConfig` as needed for your environments.
    - Update the `JWT_SECRET_KEY` in production for security purposes.
"""

import os


class Config:
    """
    Base configuration class.
    """

    DEBUG = False
    CHARGING_STATION_CSV = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data/Ladesaeulenregister.csv"
    )
    INIT_DATA = True
    JWT_SECRET_KEY = "super_secret_key"
    POSTAL_CODE_CSV = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data/datasets/geodata_berlin_plz.csv",
    )
    SERVER_PORT = 5000
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Default to in-memory database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


# class DevelopmentConfig(Config):
#    """
#    Development-specific configurations.
#    """
#    DEBUG = True
#    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/devdb"


class TestingConfig(Config):
    """
    Testing-specific configurations.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # In-memory database for tests


class TestingConfigSimple(Config):
    """
    Testing-specific configurations.
    Some test do not need to initialize all the postalcode data
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # In-memory database for tests
    INIT_DATA = False


# class ProductionConfig(Config):
#    """
#    Production-specific configurations.
#    """
#    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/proddb"
