"""Routes for ChargingStation operations.

This module provides endpoints for managing charging stations, including:
    - Retrieving all charging stations.
    - Deactivating a specific charging station.
    - Retrieving charging stations based on postal code.

Blueprints:
    - charging_stations: Blueprint for managing charging station operations.

Endpoints:
    - GET /: Retrieves all charging stations and their attributes.
    - POST /<int:station_id>/deactivate: Deactivates a specific charging station (requires authentication).
    - GET /postal_code/<int:postal_code>: Retrieves all charging stations for a given postal code.

Functions:
    - get_charging_stations: Retrieves all charging stations from the database.
    - deactivate_charging_station: Deactivates a charging station by setting its `functional` attribute to `False`.
    - get_charging_stations_by_postal_code: Retrieves charging stations associated with a specific postal code.
"""

from app.entities.charging_station import ChargingStation, db
from app.entities.postal_code import PostalCode
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

charging_stations = Blueprint("charging_stations", __name__)


@charging_stations.route("/", methods=["GET"])
def get_charging_stations():
    """Retrieve all charging stations from the database.

    Returns:
        JSON: A list of charging stations with their attributes.

    Example Response:
        [
            {
                "id": 1,
                "functional": true,
                "postal_code_id": 10115,
                "street": "Example Street",
                "house_number": "42",
                "latitude": 52.5200,
                "longitude": 13.4050
            }, ...
        ]

    Raises:
        500 Internal Server Error: If a database error occurs.
    """
    try:
        stations = ChargingStation.query.all()
        data = [
            {
                "id": station.id,
                "functional": station.functional,
                "postal_code_id": station.postal_code_id,
                "street": station.street,
                "house_number": station.house_number,
                "latitude": station.latitude,
                "longitude": station.longitude,
            }
            for station in stations
        ]
        return jsonify(data), 200
    except SQLAlchemyError as e:
        return jsonify({"error": f"Failed to retrieve charging stations: {e}"}), 500


@charging_stations.route("/<int:station_id>/deactivate", methods=["POST"])
@jwt_required()  # Requires the user to be logged in
def deactivate_charging_station(station_id):
    """Deactivate a charging station (set functional to False).

    Args:
        station_id (int): The ID of the charging station.

    Returns:
        JSON: A success message if deactivation is successful.
        JSON: An error message if the station is not found or an error occurs.

    Example Response:
        {
            "message": "Charging station 1 deactivated successfully."
        }

    Raises:
        404 Not Found: If the charging station does not exist.
        500 Internal Server Error: If a database error occurs during the update.
    """
    try:
        station = ChargingStation.query.get(station_id)
        if not station:
            return jsonify({"error": "Charging station not found."}), 404

        station.functional = False
        db.session.commit()

        return (
            jsonify(
                {"message": f"Charging station {station_id} deactivated successfully."}
            ),
            200,
        )
    except SQLAlchemyError as e:
        return jsonify({"error": f"Failed to deactivate charging station: {e}"}), 500


@charging_stations.route("/postal_code/<int:postal_code>", methods=["GET"])
def get_charging_stations_by_postal_code(postal_code):
    """Retrieve charging stations for a specific postal code.

    Args:
        postal_code (int): The postal code number.

    Returns:
        JSON: A list of charging stations that belong to the given postal code.

    Example Response:
        [
            {
                "id": 1,
                "functional": true,
                "postal_code_number": 10115,
                "street": "Example Street",
                "house_number": "42",
                "latitude": 52.5200,
                "longitude": 13.4050
            }
        ]

    Raises:
        404 Not Found: If the postal code does not exist.
        500 Internal Server Error: If a database error occurs while retrieving data.
    """
    try:
        # first is only possible due to the unique constraint of every postalcode number
        postal_code_entry = PostalCode.query.filter_by(number=postal_code).first()
        if not postal_code_entry:
            return jsonify({"error": f"Postal code {postal_code} not found."}), 404

        stations = ChargingStation.query.filter_by(
            postal_code_id=postal_code_entry.id
        ).all()
        data = [
            {
                "id": station.id,
                "functional": station.functional,
                "postal_code_number": postal_code_entry.number,
                "street": station.street,
                "house_number": station.house_number,
                "latitude": station.latitude,
                "longitude": station.longitude,
            }
            for station in stations
        ]
        return jsonify(data), 200
    except SQLAlchemyError as e:
        return (
            jsonify(
                {
                    "error": f"Failed to retrieve charging stations for postal code {postal_code}: {e}"
                }
            ),
            500,
        )
