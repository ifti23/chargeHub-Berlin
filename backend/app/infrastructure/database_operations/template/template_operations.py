from app import db  # Import your database instance
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class TemplateOperations:

    def __enter__(self):
        """
        Enter the context manager by creating a new database session.
        """
        with current_app.app_context():
            self.session = db.session
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager and ensure the session is closed.
        """
        if self.session is not None:
            self.session.close()
