from app.domain.entities.charging_station import OperationStatus
from app.infrastructure.database_operations.charging_station_operations import (
    ChargingStationOperations,
)
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, InternalServerError, NotFound


def change_charging_station_status(station_id: int, new_status: str) -> dict:
    """
    Update the operational status of a charging station.

    Args:
        station_id (int): The ID of the charging station.
        new_status (str): The new operational status.

    Returns:
        str: A success message.

    Raises:
        BadRequest: If the status is invalid.
        NotFound: If the station is not found.
        InternalServerError: If the update fails.
    """
    if new_status.upper() not in OperationStatus.__members__:
        raise BadRequest(
            "Invalid status. Must be one of: operational, used, malfunctioning."
        )

    try:
        with ChargingStationOperations() as repository:
            station = repository.get_charging_station_by_id(station_id)
            if not station:
                raise NotFound(f"Charging station with ID {station_id} not found.")

            # Update the status
            repository.update_charging_station_status(station, new_status)
            return {
                "message": f"Success: Charging station {station_id} updated to {new_status} successfully."
            }

    except SQLAlchemyError as e:
        raise InternalServerError(f"Failed to update charging station: {e}")
