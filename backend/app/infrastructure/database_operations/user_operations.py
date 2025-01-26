from app.domain.entities.user import User, UserValidationError
from app.infrastructure.database_operations.template.template_operations import (
    TemplateOperations,
)


class UserOperations(TemplateOperations):

    def get_user_by_username_or_email(self, username_or_email: str) -> User:
        """
        Retrieve a user by username or email.

        Args:
            username_or_email (str): The username or email to search.

        Returns:
            User: The user object if found, None otherwise.
        """

        return (
            self.session.query(User)
            .filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            )
            .first()
        )

    def user_exists(self, email: str, username: str) -> bool:
        """
        Check if a user with the given email already exists.

        Args:
            email (str): The email to check.
            username (str): The username to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        found_e_mail = self.session.query(User).filter_by(email=email).first()
        found_username = self.session.query(User).filter_by(username=username).first()

        return found_username is not None or found_e_mail is not None

    def add_user(self, user_data: dict) -> int:
        """
        Add a new user to the database.

        Args:
            user_data (dict): A dictionary containing user details, including optional 'phone_number'.

        Returns:
            int: The ID of the newly created user.
        """
        if self.user_exists(user_data["email"], user_data["username"]):
            raise UserValidationError("A user with this email already exists.")

        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
            phone_number=user_data.get(
                "phone_number"
            ),  # Include phone_number if provided
        )
        self.session.add(new_user)
        self.session.commit()
        return new_user.id
