"""Postal Code entity module.
Defines how a postal code is defined.

Classes:
    PostalCodeValidationError: Custom exception for postal code validation errors.
    PostalCode: Database model for postal codes.
"""

import re

from app.domain.entities.templates.base import BaseModel, db
from sqlalchemy import Integer, Text


class PostalCodeValidationError(Exception):
    """
    Custom exception for postal code validation errors.
    """

    pass


RE_POLYGON_VALIDATION_REGEX = (
    r"^POLYGON \(\((\d+\.\d+\s\d+\.\d+,\s)*\d+\.\d+\s\d+\.\d+\)\)$"
)


class PostalCode(BaseModel):
    """
    Model for PostalCode.

    Attributes:
        number (int): The postal code number.
        polygon (str): The polygon data as WKT (Well-Known Text).
    """

    __tablename__ = "postal_codes"

    number = db.Column(Integer, nullable=False, unique=True)
    polygon = db.Column(Text, nullable=False)

    def __init__(self, number: int, polygon: str):
        if not self.number_is_valid(number):
            raise PostalCodeValidationError(
                "Postal code must be between 10115 and 14199."
            )
        if not self.polygon_is_valid(polygon):
            raise PostalCodeValidationError(
                "Polygon must be a valid WKT format: 'Polygon ((x1 y1, x2 y2, ...))'."
            )
        self.number = number
        self.polygon = polygon

    @staticmethod
    def number_is_valid(number: int) -> bool:
        """
        Validate the postal code number.

        Args:
            number (int): The postal code number.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not isinstance(number, int):
            return False
        return 10115 <= number <= 14199

    @staticmethod
    def polygon_is_valid(polygon: str) -> bool:
        """
        Validate the polygon string.

        Args:
            polygon (str): The polygon data as WKT.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not isinstance(polygon, str):
            return False
        return re.match(RE_POLYGON_VALIDATION_REGEX, polygon) is not None
