"""Routes for PostalCode operations.

This module provides endpoints for retrieving postal code data.
User additions or modifications of postal code data are not supported
as the data is intended to be managed internally.

Blueprints:
    - get_postal_codes: Blueprint for managing postal code operations.

Endpoints:
    - GET /: Retrieves all postal codes and their polygons.

Functions:
    - get_all_postal_codes: Fetches all postal codes with their polygon data.
"""

from app.entities.postal_code import PostalCode
from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError

get_postal_codes = Blueprint("get_postal_codes", __name__)


@get_postal_codes.route("/", methods=["GET"])
def get_all_postal_codes():
    """
    Retrieve all postal codes and their polygons.

    Returns:
        JSON: A list of postal codes with their associated polygon data.

    For a detailed view of the polygon data, please refer to data/datasets/geodata_berlin_plz.csv
    Example Response:
        [
            {
                "number": 10115,
                "polygon": "POLYGON ((...))"
            },
            {
                "number": 10117,
                "polygon": "POLYGON ((...))"
            }
        ]

    Raises:
        500 Internal Server Error: If a database error occurs.

    Error Response:
        {
            "error": "Database error: <error_message>"
        }
    """
    try:
        postal_codes = PostalCode.query.all()
        data = [{"number": pc.number, "polygon": pc.polygon} for pc in postal_codes]
        return jsonify(data), 200
    except SQLAlchemyError as e:
        return jsonify({"error": f"Database error: {e}"}), 500
