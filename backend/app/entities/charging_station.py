from app.entities.base import BaseModel, db
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ChargingStationValidationError(Exception):
    """
    Custom exception for charging station validation errors.
    """

    pass


class ChargingStation(BaseModel):
    """
    Model for ChargingStation.

    Attributes:
        functional (bool): Indicates if the charging station is functional.
        postal_code_id (int): Foreign key to PostalCode.
        postal_code (PostalCode): Relationship to the PostalCode entity. THis is SQLAlchemy specific
        street (str): Street name of the charging station.
        house_number (str): House number of the charging station.
        latitude (float): Latitude of the charging station location.
        longitude (float): Longitude of the charging station location.
    """

    __tablename__ = "charging_stations"

    functional = db.Column(Boolean, nullable=False, default=True)
    postal_code_id = db.Column(Integer, ForeignKey("postal_codes.id"), nullable=False)
    postal_code = relationship("PostalCode", backref="charging_stations")
    street = db.Column(String(255), nullable=False)
    house_number = db.Column(String(50), nullable=True)
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)

    def __init__(
        self,
        functional: bool,
        postal_code_id: int,
        street: str,
        house_number: str,
        latitude: float,
        longitude: float,
    ):
        if not self.is_valid_latitude(latitude):
            raise ChargingStationValidationError("Latitude must be between -90 and 90.")
        if not self.is_valid_longitude(longitude):
            raise ChargingStationValidationError(
                "Longitude must be between -180 and 180."
            )

        self.functional = functional
        self.postal_code_id = postal_code_id
        self.street = street
        self.house_number = house_number
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def is_valid_latitude(latitude: float) -> bool:
        """
        Validate the latitude value.

        Args:
            latitude (float): Latitude value.

        Returns:
            bool: True if valid, False otherwise.
        """
        return -90 <= latitude <= 90

    @staticmethod
    def is_valid_longitude(longitude: float) -> bool:
        """
        Validate the longitude value.

        Args:
            longitude (float): Longitude value.

        Returns:
            bool: True if valid, False otherwise.
        """
        return -180 <= longitude <= 180
