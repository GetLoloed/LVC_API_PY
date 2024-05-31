"""
Schéma pour les éléments.
"""

from pydantic import BaseModel


class ItemSchema(BaseModel):
    """
    Schéma pour représenter un élément.
    """
    name: str
    description: str = None
    price: float
    is_available: bool = True

    class Config:  # pylint: disable=too-few-public-methods
        """
        Configurations pour le schéma de l'élément.
        """
        from_attributes = True
