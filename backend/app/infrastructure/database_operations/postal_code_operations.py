from app.domain.entities.postal_code import PostalCode
from app.infrastructure.database_operations.template.template_operations import (
    TemplateOperations,
)


class PostalCodeOperations(TemplateOperations):

    def get_postal_code_details(self, postal_code: str) -> dict:
        """
        Retrieve details for a postal code.

        Args:
            postal_code (str): The postal code to search.

        Returns:
            dict: Postal code details as a dictionary, or None if not found.
        """
        postal_code_entry = (
            self.session.query(PostalCode).filter_by(number=postal_code).first()
        )

        if postal_code_entry:
            return {
                "number": postal_code_entry.number,
                "polygon": postal_code_entry.polygon,
            }

        return {}

    def is_valid(self, postal_code: str) -> bool:
        """
        Check if the given postal code exists in the database.

        Args:
            postal_code (str): The postal code to validate.

        Returns:
            bool: True if the postal code exists, False otherwise.
        """
        try:
            postal_code = int(postal_code)
        except ValueError:
            return False

        if PostalCode.number_is_valid(postal_code):
            # Query the database to check for existence
            exists = (
                self.session.query(PostalCode).filter_by(number=postal_code).first()
            )
            return exists is not None
        return False
