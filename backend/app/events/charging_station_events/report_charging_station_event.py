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

from app.domain.services.charging_staion_services.report_charging_station_service import (
    change_charging_station_status,
)
from flask import jsonify, request
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from . import charging_stations


@charging_stations.route("/change_status", methods=["POST"])
def report_charging_station_event():
    """
    Update the operational status of a charging station.

    Returns:
        JSON: A success message if the update is successful.
        JSON: An error message if the station is not found or an error occurs.
    """
    try:
        station_id = request.args.get("station_id", type=int)
        new_status = request.args.get("new_status", type=str)

        if not station_id or not new_status:
            raise BadRequest("Both 'station_id' and 'new_status' are required.")

        # Delegate to the service layer
        message = change_charging_station_status(station_id, new_status)
        return jsonify({"message": message}), 200

    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except InternalServerError as e:
        return jsonify({"error": str(e)}), 500
