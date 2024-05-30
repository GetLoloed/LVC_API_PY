from sqlalchemy.orm import Session
from models.item_model import Item


class ItemRepository:

    def __init__(self, db: Session):
        self.db = db  # initialiser la session de base de données

    def get_all(self):
        return self.db.query(Item).all()  # obtenir tous les éléments

    def create(self, item: Item) -> Item:
        self.db.add(item)  # ajouter l'élément à la base de données
        self.db.commit()  # confirmer la transaction
        self.db.refresh(item)  # rafraîchir l'élément avec l'état actuel de la base de données
        return item  # renvoyer l'élément créé

    def read(self, item_id: int) -> Item:
        # récupérer l'élément par son identifiant
        return self.db.query(Item).filter(Item.id == item_id).first()

    def update(self, item: Item) -> Item:
        # rechercher l'élément dans la base de données par son identifiant
        db_item = self.db.query(Item).filter(Item.id == item.id).first()
        if db_item:
            # mettre à jour les propriétés de l'élément avec celles de l'élément passé en argument
            db_item.name = item.name
            db_item.description = item.description
            db_item.price = item.price
            db_item.is_available = item.is_available
            self.db.commit()  # confirmer la transaction
            self.db.refresh(db_item)  # rafraîchir l'élément avec l'état actuel de la base de données
            return db_item  # renvoyer l'élément mis à jour

    def delete(self, item_id: int) -> None:
        # rechercher l'élément à supprimer par son identifiant
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            self.db.delete(item)  # supprimer l'élément de la base de données
            self.db.commit()  # confirmer la transaction
