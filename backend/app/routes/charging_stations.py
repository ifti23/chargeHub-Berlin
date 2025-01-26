"""Routes for ChargingStation operations.

This module provides endpoints for managing charging stations, including:
    - Retrieving all charging stations.
    - Deactivating a specific charging station.
    - Retrieving charging stations based on postal code.

Blueprints:
    - charging_stations: Blueprint for managing charging station operations.

Endpoints:
    - GET /: Retrieves all charging stations and their attributes.
    - POST /deactivate?station_id=<int:station_id>&new_status=operational: Deactivates a specific charging station (requires authentication).
    - GET /postal_code/<int:postal_code>: Retrieves all charging stations for a given postal code.

Functions:
    - get_charging_stations: Retrieves all charging stations from the database.
    - deactivate_charging_station: Deactivates a charging station by setting its `functional` attribute to `False`.
    - get_charging_stations_by_postal_code: Retrieves charging stations associated with a specific postal code.
"""

from app.entities.charging_station import ChargingStation, db, OperationStatus
from app.entities.postal_code import PostalCode
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

charging_stations = Blueprint("charging_stations", __name__)


def serialize_charging_station(station: ChargingStation) -> dict:
    """Serialize a ChargingStation object to a dictionary for JSON response."""
    return {
        "id": station.id,
        "functional": str(station.functional),
        "postal_code_id": station.postal_code_id,
        "street": station.street,
        "house_number": station.house_number,
        "latitude": station.latitude,
        "longitude": station.longitude,
        "operator": station.operator,
        "address_suffix": station.address_suffix,
        "nominal_power": station.nominal_power,
        "charging_type": str(station.charging_type),
        "num_charging_points": station.num_charging_points,
    }


@charging_stations.route("/", methods=["GET"])
def get_charging_stations():
    """Retrieve all charging stations from the database.

    Returns:
        JSON: A list of charging stations with their attributes.

    Example URL:
        http://127.0.0.1:5000/api/charging_stations/

    Example Response:
        [
            {
                "id": 1,
                "functional": FunctionalStatus[operational, used, malfunctioning],
                "postal_code_number": 10115,
                "street": "Example Street",
                "house_number": "42",
                "latitude": 52.5200,
                "longitude": 13.4050,
                "operator": "Operator Name",
                "address_suffix": "Near Mall",
                "nominal_power": 50.0,
                "charging_type": "Fast",
                "num_charging_points": 4
            }, ...
        ]

    Raises:
        500 Internal Server Error: If a database error occurs.
    """
    try:
        stations = ChargingStation.query.all()
        data = [serialize_charging_station(station) for station in stations]
        return jsonify(data), 200
    except SQLAlchemyError as e:
        return jsonify({"error": f"Failed to retrieve charging stations: {e}"}), 500


@charging_stations.route("/change_status", methods=["POST"])
def deactivate_charging_station():
    """Update the operational status of a charging station.

    Query Parameters:
        station_id (int): The ID of the charging station.
        new_status (str): The new operational status for the charging station.

    Returns:
        JSON: A success message if the update is successful.
        JSON: An error message if the station is not found or an error occurs.

    Example URL:
        http://127.0.0.1:5000/api/charging_stations/deactivate?station_id=1&new_status=operational

    Example Response:
        {
            "message": "Charging station 1 updated to operational successfully."
        }

    Raises:
        404 Not Found: If the charging station does not exist.
        400 Bad Request: If the provided status is invalid.
        500 Internal Server Error: If a database error occurs during the update.
    """
    try:
        station_id = request.args.get("station_id", type=int)
        new_status = request.args.get("new_status", type=str)

        if not station_id or not new_status:
            return (
                jsonify({"error": "Both 'station_id' and 'new_status' are required."}),
                400,
            )

        station = ChargingStation.query.get(station_id)
        if not station:
            return jsonify({"error": "Charging station not found."}), 404

        if new_status.upper() not in OperationStatus.__members__:
            return (
                jsonify(
                    {
                        "error": "Invalid status. Must be one of: operational, used, malfunctioning."
                    }
                ),
                400,
            )

        # Update the station's functional status
        station.functional = OperationStatus[new_status.upper()]
        db.session.commit()

        return (
            jsonify(
                {
                    "message": f"Charging station {station_id} updated to {new_status} successfully."
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        return jsonify({"error": f"Failed to update charging station: {e}"}), 500


@charging_stations.route("/postal_code/<int:postal_code>", methods=["GET"])
def get_charging_stations_by_postal_code(postal_code):
    """Retrieve charging stations for a specific postal code.

    Args:
        postal_code (int): The postal code number.

    Returns:
        JSON: A list of charging stations that belong to the given postal code.

    Example URL:
        http://127.0.0.1:5000/api/charging_stations/postal_code/10115

    Example Response:
        [
            {
                "id": 1,
                "functional": true,
                "postal_code_number": 10115,
                "street": "Example Street",
                "house_number": "42",
                "latitude": 52.5200,
                "longitude": 13.4050,
                "operator": "Operator Name",
                "address_suffix": "Near Mall",
                "nominal_power": 50.0,
                "charging_type": "fast",
                "num_charging_points": 4
            }
        ]

    Raises:
        404 Not Found: If the postal code does not exist.
        500 Internal Server Error: If a database error occurs while retrieving data.
    """
    try:
        postal_code_entry = PostalCode.query.filter_by(number=postal_code).first()
        if not postal_code_entry:
            return jsonify({"error": f"Postal code {postal_code} not found."}), 404

        stations = ChargingStation.query.filter_by(
            postal_code_id=postal_code_entry.id
        ).all()
        data = [serialize_charging_station(station) for station in stations]
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
