from app.infrastructure.database_operations.charging_station_operations import (
    ChargingStationOperations,
)
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError


def get_all_charging_stations() -> dict:
    """Get all charging stations

    Returns:
        dict: Postal code details if found.

    Raises:
        InternalServerError: If the postal code does not exist in the database.
    """
    try:
        with ChargingStationOperations() as repository:
            found_charging_stations = repository.get_all_charging_stations()

    except SQLAlchemyError as db_err:
        raise InternalServerError(f"Database error: {db_err}")

    return {
        "message": "Successfully found charging stations.",
        "stations": found_charging_stations,
    }
