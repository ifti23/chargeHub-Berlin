from app.domain.entities.charging_station import ChargingStation, OperationStatus
from app.infrastructure.database_operations.template.template_operations import (
    TemplateOperations,
)
from sqlalchemy.exc import SQLAlchemyError


class ChargingStationOperations(TemplateOperations):

    def get_all_charging_stations(self) -> list[dict]:
        """Retrieve all charging stations

        Returns:
            list: A list of all charging stations as dictionaries.
        """
        stations = self.session.query(ChargingStation).all()
        return [station.get_dict() for station in stations]

    def get_charging_stations_by_postal_code(
        self, postal_code: [str | int]
    ) -> list[dict]:
        """Retrieve charging stations linked to a postal code.

        Args:
            postal_code (str): A valid postal code

        Returns:
            list: A list of charging stations as dictionaries.
        """

        if not isinstance(postal_code, (str, int)):
            raise TypeError("Postal code must be a string or integer.")
        try:
            if isinstance(postal_code, str):
                postal_code = int(postal_code)
        except ValueError:
            raise ValueError("Postal code must be given as valid integer.")

        stations = (
            self.session.query(ChargingStation)
            .filter_by(postal_code_id=postal_code)
            .all()
        )

        return [station.get_dict() for station in stations]

    def get_charging_station_by_id(self, station_id: int) -> ChargingStation:
        return self.session.query(ChargingStation).filter_by(id=station_id).first()

    def update_charging_station_status(
        self, station: ChargingStation, new_status: str
    ) -> None:
        """
        Update the operational status of a charging station.

        Args:
            station (ChargingStation): The charging station object to update.
            new_status (str): The new operational status.

        Raises:
            SQLAlchemyError: If the update fails.
        """
        try:
            station.functional = OperationStatus[new_status.upper()]
            self.session.commit()
        except SQLAlchemyError as e:
            # allways rollback if an error occurs
            self.session.rollback()
            raise SQLAlchemyError(f"Error updating charging station: {e}")
