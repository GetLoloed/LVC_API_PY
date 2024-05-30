from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from repositories.item_repository import ItemRepository
from models.item_model import Item
from schemas.item_schema import ItemSchema
from db.database import SessionLocal
from typing import List
from fastapi import Body

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/items/", response_model=List[ItemSchema])
def get_all_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    item_repository = ItemRepository(db)
    items = item_repository.get_all(skip=skip, limit=limit)
    return items


@router.post("/items/", response_model=ItemSchema)
def create_item(item: ItemSchema = Body(...), db: Session = Depends(get_db)):
    item_repository = ItemRepository(db)
    created_item = item_repository.create(Item(**item.dict()))
    return created_item


@router.get("/items/{item_id}", response_model=ItemSchema)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item_repository = ItemRepository(db)
    item = item_repository.read(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/items/{item_id}", response_model=ItemSchema)
def update_item(item_id: int, item: ItemSchema, db: Session = Depends(get_db)):
    item_repository = ItemRepository(db)
    updated_item = item_repository.update(Item(id=item_id, **item.dict()))
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item_repository = ItemRepository(db)
    item_repository.delete(item_id)
    return {"message": "Item deleted"}


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(Item).offset(skip).limit(limit).all()

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
