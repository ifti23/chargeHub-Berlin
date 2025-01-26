from app.domain.services.charging_staion_services.charging_stations_get_all_service import (
    get_all_charging_stations,
)
from flask import jsonify
from werkzeug.exceptions import InternalServerError

from . import charging_stations


@charging_stations.route("/", methods=["GET"])
def init_ui_charging_stations_event():
    """
    Retrieve all postal codes and their polygons.

    Returns:
        JSON: A list of postal codes with their associated polygon data.
    """
    try:
        # Delegate to the service layer
        found_charging_stations = get_all_charging_stations()
        return jsonify(found_charging_stations), 200

    except InternalServerError as e:
        return jsonify({"error": str(e)}), 500
