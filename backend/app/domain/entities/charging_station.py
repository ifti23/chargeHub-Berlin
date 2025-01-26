from enum import Enum

from app.domain.entities.templates.base import BaseModel, db
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ENUM as SQLAlchemyEnum
from sqlalchemy.orm import relationship


class OperationStatus(Enum):
    OPERATIONAL = "operational"
    USED = "used"
    MALFUNCTIONING = "malfunctioning"

    def __str__(self):
        return self.value


class ChargingType(Enum):
    FAST = "fast"
    NORMAL = "normal"

    def __str__(self):
        return self.value

    @staticmethod
    def convert(value: str):
        match value:
            case "Normalladeeinrichtung":
                return ChargingType.NORMAL
            case "Schnellladeeinrichtung":
                return ChargingType.FAST
            case _:
                return None


class ChargingStationValidationError(Exception):
    """
    Custom exception for charging station validation errors.
    """

    pass


class ChargingStation(BaseModel):
    """
    Model for ChargingStation.

    Attributes:
        functional (OperationStatus): Indicates the status of the charging station.
        postal_code_id (int): Foreign key to PostalCode.
        postal_code (PostalCode): Relationship to the PostalCode entity. This is SQLAlchemy specific
        street (str): Street name of the charging station.
        house_number (str): House number of the charging station.
        latitude (float): Latitude of the charging station location.
        longitude (float): Longitude of the charging station location.
        operator (str): Operator of the charging station.
        address_suffix (str): Additional address details.
        nominal_power (int): Nominal power of the charging station (in kW).
        charging_type (ChargingType): Type of the charging station (e.g., fast, normal).
        num_charging_points (int): Number of charging points at the station.
    """

    __tablename__ = "charging_stations"

    functional = db.Column(
        SQLAlchemyEnum(OperationStatus),
        nullable=False,
        default=OperationStatus.OPERATIONAL,
    )
    postal_code_id = db.Column(Integer, ForeignKey("postal_codes.id"), nullable=False)
    postal_code = relationship("PostalCode", backref="charging_stations")
    street = db.Column(String(255), nullable=False)
    house_number = db.Column(String(50), nullable=True)
    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)
    operator = db.Column(String(255), nullable=True)
    address_suffix = db.Column(String(255), nullable=True)
    nominal_power = db.Column(Integer, nullable=True)
    charging_type = db.Column(SQLAlchemyEnum(ChargingType), nullable=True)
    num_charging_points = db.Column(Integer, nullable=True)

    def __init__(
        self,
        functional: OperationStatus,
        postal_code_id: int,
        street: str,
        house_number: str,
        latitude: float,
        longitude: float,
        operator: str = None,
        address_suffix: str = None,
        nominal_power: int = None,
        charging_type: ChargingType = None,
        num_charging_points: int = None,
    ):
        # Validate and convert the `functional` field
        if isinstance(functional, str):
            try:
                functional = OperationStatus[functional.upper()]
            except KeyError:
                raise ChargingStationValidationError(
                    f"Invalid functional status: {functional}. "
                    f"Must be one of: {[status.value for status in OperationStatus]}"
                )
        elif not isinstance(functional, OperationStatus):
            raise ChargingStationValidationError(
                f"Invalid type for functional status: {functional}. Must be a valid OperationStatus."
            )

        if not self.is_valid_latitude(latitude):
            raise ChargingStationValidationError("Latitude must be between -90 and 90.")
        if not self.is_valid_longitude(longitude):
            raise ChargingStationValidationError(
                "Longitude must be between -180 and 180."
            )
        if not self.is_valid_nominal_power(nominal_power):
            raise ChargingStationValidationError(
                "Nominal power must be a positive integer greater than 0."
            )
        if not self.is_valid_num_charging_points(num_charging_points):
            raise ChargingStationValidationError(
                "Number of charging points must be a positive integer greater than 0."
            )
        if not self.is_valid_operator(operator):
            raise ChargingStationValidationError("Operator must be a non-empty string.")
        if not self.is_valid_address_suffix(address_suffix):
            raise ChargingStationValidationError(
                "Address suffix must be a string or None."
            )

        self.functional = functional
        self.postal_code_id = postal_code_id
        self.street = street
        self.house_number = house_number
        self.latitude = latitude
        self.longitude = longitude
        self.operator = operator
        self.address_suffix = address_suffix
        self.nominal_power = nominal_power
        self.charging_type = charging_type
        self.num_charging_points = num_charging_points

    def get_dict(self):
        return {
            "id": self.id,
            "functional": str(self.functional),
            "postal_code_id": self.postal_code_id,
            "street": self.street,
            "house_number": self.house_number,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "operator": self.operator,
            "address_suffix": self.address_suffix,
            "nominal_power": self.nominal_power,
            "charging_type": str(self.charging_type),
            "num_charging_points": self.num_charging_points,
        }

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

    @staticmethod
    def is_valid_nominal_power(nominal_power: int) -> bool:
        """
        Validate the nominal power value.

        Args:
            nominal_power (int): Nominal power value.

        Returns:
            bool: True if valid, False otherwise.
        """
        return nominal_power is not None and nominal_power > 0

    @staticmethod
    def is_valid_num_charging_points(num_charging_points: int) -> bool:
        """
        Validate the number of charging points.

        Args:
            num_charging_points (int): Number of charging points.

        Returns:
            bool: True if valid, False otherwise.
        """
        return (
            num_charging_points is not None
            and isinstance(num_charging_points, int)
            and num_charging_points > 0
        )

    @staticmethod
    def is_valid_operator(operator: str) -> bool:
        """
        Validate the operator value.

        Args:
            operator (str): Operator value.

        Returns:
            bool: True if valid, False otherwise.
        """
        return (
            operator is not None
            and isinstance(operator, str)
            and len(operator.strip()) > 0
        )

    @staticmethod
    def is_valid_address_suffix(address_suffix: str) -> bool:
        """
        Validate the address suffix value.

        Args:
            address_suffix (str): Address suffix value.

        Returns:
            bool: True if valid, False otherwise.
        """
        return address_suffix is None or isinstance(address_suffix, str)
