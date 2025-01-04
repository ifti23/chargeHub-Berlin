"""Application factory module.
Defines the `create_app` function for initializing the Flask application.
Reads in the configuration from app/config.py

Functions:
    load_charging_stations_data:    load all charging stations to database
    load_postal_code_data:          load all postal codes to database
    create_app:                     creates and configures the Flask app.
"""

import csv
import os

from app.entities.charging_station import ChargingStation
from app.entities.postal_code import PostalCode, db
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError


def load_charging_stations_data(application):
    """
    Load charging station data from the CSV file into the database.

    Args:
        application (Flask): The Flask application instance.
    """
    file_path = os.path.abspath(application.config.get("CHARGING_STATION_CSV"))
    with application.app_context():
        try:
            with open(file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile, delimiter=";")
                for row in reader:
                    # Filter only entries where Bundesland is Berlin
                    try:
                        if not PostalCode.number_is_valid(int(row["Postleitzahl"])):
                            continue
                    except (TypeError, ValueError):
                        continue

                    postal_code = PostalCode.query.filter_by(
                        number=int(row["Postleitzahl"])
                    ).first()
                    if not postal_code:
                        application.logger.warning(
                            f"Postal code {row['Postleitzahl']} not found in the database."
                        )
                        continue

                    latitude = float(row["Breitengrad"].replace(",", "."))
                    longitude = float(row["Längengrad"].replace(",", "."))

                    charging_station = ChargingStation(
                        functional=True,
                        postal_code_id=postal_code.id,
                        street=row["Straße"],
                        house_number=row["Hausnummer"],
                        latitude=latitude,
                        longitude=longitude,
                    )
                    db.session.add(charging_station)
                db.session.commit()
        except FileNotFoundError:
            application.logger.error(f"CSV file not found at {file_path}")
        except csv.Error as csv_err:
            application.logger.error(f"Error processing CSV file: {csv_err}")
        except SQLAlchemyError as db_err:
            application.logger.error(f"Database error: {db_err}")


def load_postal_code_data(application):
    """
    Load postal codes and their polygons into the database from a CSV file.

    Args:
        application (Flask): The Flask application instance.
    """
    file_path = os.path.abspath(application.config.get("POSTAL_CODE_CSV"))
    with application.app_context():
        try:
            with open(file_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, delimiter=";")
                next(reader, None)  # Skip the header row
                for row in reader:
                    try:
                        number = int(row[0])
                        polygon = row[1]
                        if not PostalCode.query.filter_by(number=number).first():
                            postal_code = PostalCode(number=number, polygon=polygon)
                            db.session.add(postal_code)
                    except ValueError as ve:
                        application.logger.error(f"Data format error in CSV file: {ve}")
                db.session.commit()
        except FileNotFoundError as fnfe:
            application.logger.error(f"CSV file not found: {file_path}, Error: {fnfe}")
        except IOError as ioe:
            application.logger.error(
                f"Error reading the file: {file_path}, Error: {ioe}"
            )
        except SQLAlchemyError as sqle:
            db.session.rollback()  # Rollback the transaction to maintain database integrity
            application.logger.error(
                f"Database error during postal code loading: {sqle}"
            )


def create_app(config_class="config.Config"):
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """
    application = Flask(__name__)
    application.config.from_object(config_class)
    CORS(application)
    # Add a secret key for JWT
    application.config["JWT_SECRET_KEY"] = (
        "your_secret_key"  # Replace with a secure key
    )

    JWTManager(application)  # Initialize JWT

    # Initialize the database
    db.init_app(application)
    with application.app_context():
        db.create_all()
        inspector = inspect(db.engine)
        application.logger.debug(f"Existing tables: {inspector.get_table_names()}")
    if application.config.get("INIT_DATA"):
        load_postal_code_data(application)
        load_charging_stations_data(application)

    # Register Blueprints
    from app.routes.charging_stations import charging_stations
    from app.routes.postal_codes import get_postal_codes
    from app.routes.users import get_users, login_user, register_user

    application.register_blueprint(
        charging_stations, url_prefix="/api/charging_stations"
    )
    application.register_blueprint(get_users, url_prefix="/api/users")
    application.register_blueprint(register_user, url_prefix="/api/register_user")
    application.register_blueprint(login_user, url_prefix="/api/login_user")
    application.register_blueprint(get_postal_codes, url_prefix="/api/postal_codes")

    return application
