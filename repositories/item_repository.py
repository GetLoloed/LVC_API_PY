"""
Module de gestion des opérations CRUD pour les articles.
"""

from sqlalchemy.orm import Session
from models.item_model import Item


class ItemRepository:
    """
    Classe pour interagir avec la base de données des articles.
    """

    def __init__(self, db: Session):
        """
        Initialiser la session de base de données.
        """
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 10):
        """
        Obtenir tous les articles de la base de données.

        :param skip: Le nombre d'articles à sauter.
        :param limit: Le nombre d'articles à récupérer.
        :return: La liste des articles.
        """
        return self.db.query(Item).offset(skip).limit(limit).all()

    def create(self, item: Item) -> Item:
        """
        Créer un nouvel article dans la base de données.

        :param item: L'article à ajouter.
        :return: L'article créé.
        """
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def read(self, item_id: int) -> Item:
        """
        Lire un article spécifique par ID.

        :param item_id: L'ID de l'article.
        :return: L'article trouvé ou None.
        """
        return self.db.query(Item).filter(Item.id == item_id).first()

    def update(self, item: Item) -> Item:
        """
        Mettre à jour un article existant.

        :param item: L'article avec les nouvelles données.
        :return: L'article mis à jour ou None.
        """
        db_item = self.db.query(Item).filter(Item.id == item.id).first()
        if db_item:
            db_item.name = item.name
            db_item.description = item.description
            db_item.price = item.price
            db_item.is_available = item.is_available
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        return None

    def delete(self, item_id: int) -> None:
        """
        Supprimer un article par ID.

        :param item_id: L'ID de l'article à supprimer.
        """
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            self.db.delete(item)
            self.db.commit()
