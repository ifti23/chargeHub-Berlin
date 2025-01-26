from app.infrastructure.database_operations.charging_station_operations import (
    ChargingStationOperations,
)
from app.infrastructure.database_operations.postal_code_operations import (
    PostalCodeOperations,
)
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import InternalServerError, NotFound


def search_postal_code_service(postal_code: str) -> dict:
    """
    Search for postal code details.

    Args:
        postal_code (str): The postal code to search for.

    Returns:
        dict: Postal code details if found.

    Raises:
        NotFound: If the postal code does not exist in the database.
    """
    try:
        with PostalCodeOperations() as repository:
            if not repository.is_valid(postal_code):
                raise NotFound(f"given postal_code is not valid: {postal_code}")

        with ChargingStationOperations() as repository:
            found_charging_stations = repository.get_charging_stations_by_postal_code(
                postal_code
            )
    except SQLAlchemyError as e:
        raise InternalServerError(f"Database error: {str(e)}")

    return {
        "message": "Successfully found charging stations.",
        "stations": found_charging_stations,
    }
