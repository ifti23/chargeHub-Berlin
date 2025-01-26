from app.domain.services.charging_staion_services.postal_code_search_service import (
    search_postal_code_service,
)
from flask import jsonify, request
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound

from . import charging_stations


@charging_stations.route("/postal_code/<int:postal_code>", methods=["GET"])
def search_postal_code_event(postal_code: [int | str]):
    """
    Search for postal code details.

    Returns:
        JSON: Postal code details if found.
        JSON: An error message with status 404 if not found.
    """
    try:
        if not isinstance(postal_code, (int, str)):
            raise TypeError

        if not str(postal_code).isnumeric():
            raise ValueError

        if not postal_code:
            raise BadRequest("'postal_code' is required.")

        found_charging_stations = search_postal_code_service(str(postal_code))
        return jsonify(found_charging_stations), 200

    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input data."}), 400
    except NotFound as e:
        return jsonify({"error": str(e)}), 404
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except InternalServerError as e:
        return jsonify({"error": "An unexpected error occurred."}), 500
