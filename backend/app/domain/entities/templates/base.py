"""
Base module for database setup.
Defines a SQLAlchemy BaseModel for use across application entities.

Classes:
    BaseModel: Abstract base class for all database tables.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    """
    Abstract base model class with common attributes for all tables.

    Attributes:
        id (int): Primary key.
        Possible features:
            #created_at (DateTime): Timestamp of creation.
            #updated_at (DateTime): Timestamp of last update.
    """

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    # created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
