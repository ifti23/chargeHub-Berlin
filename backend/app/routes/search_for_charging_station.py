from flask import Flask, jsonify, request
from flask import Blueprint, jsonify

search_station_plz = Blueprint("search_station_plz", __name__)
search_stations = Blueprint("search_station_plz", __name__)


@search_station_plz.route("/", methods=["GET"])
def search():
    """Get all stations within a given postalcode"""
    search_id = request.args.get("plz", type=int)
    if not 10114 < search_id < 14200:
        return (
            jsonify(
                {
                    "error": "The given postal code needs to be from berlin (between 10115 and 14199)"
                }
            ),
            400,
        )

    return jsonify({"message": "Inserted a valid postal code"})


@search_stations.route("/", methods=["GET"])
def get_all_stations():
    """Get all stations from all postalcodes"""
    return jsonify({"message": "Here are all stations"})
