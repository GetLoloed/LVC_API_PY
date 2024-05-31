"""
This module defines the Item model for SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean
from db.database import Base


class Item(Base):
    """
    The Item class represents the items table in the database.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    is_available = Column(Boolean, default=True)
