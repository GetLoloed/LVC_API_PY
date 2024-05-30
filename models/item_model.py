from sqlalchemy import Column, Integer, String, Float, Boolean
from db.database import Base


# Définition de notre modèle d'élément pour SQLAlchemy
class Item(Base):
    __tablename__ = "items"  # le nom de la table dans la base de données

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # l'id est la clé primaire, auto-incrementée
    name = Column(String, index=True)  # le nom de l'élément, une chaîne de caractères qui sera indexée
    description = Column(String, index=True)  # description de l'élément, c'est aussi une chaîne de caractères indexée
    price = Column(Float)  # le prix de l'élément, un nombre flottant
    is_available = Column(Boolean,
                          default=True)  # un indicateur pour savoir si l'élément est disponible ou pas, par défaut c'est True
