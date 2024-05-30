from sqlalchemy.orm import Session
from models.item_model import Item


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Item).all()

    def create(self, item: Item) -> Item:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def read(self, item_id: int) -> Item:
        return self.db.query(Item).filter(Item.id == item_id).first()

    def update(self, item: Item) -> Item:
        db_item = self.db.query(Item).filter(Item.id == item.id).first()
        if db_item:
            db_item.name = item.name
            db_item.description = item.description
            db_item.price = item.price
            db_item.is_available = item.is_available
            self.db.commit()
            self.db.refresh(db_item)
            return db_item

    def delete(self, item_id: int) -> None:
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            self.db.delete(item)
            self.db.commit()
