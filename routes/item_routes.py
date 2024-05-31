from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from repositories.item_repository import ItemRepository
from models.item_model import Item
from schemas.item_schema import ItemSchema
from db.database import SessionLocal
from typing import List
from fastapi import Body

router = APIRouter()


# Définition de la dépendance pour obtenir la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Route pour obtenir tous les articles
@router.get("/items/", response_model=List[ItemSchema])
def get_all_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    item_repository = ItemRepository(db)
    items = item_repository.get_all(skip=skip, limit=limit)
    return items


# Route pour créer un nouvel article
@router.post("/items/", response_model=ItemSchema)
def create_item(item: ItemSchema = Body(...), db: Session = Depends(get_db)):
    item_repository = ItemRepository(db)
    created_item = item_repository.create(Item(**item.dict()))
    return created_item


# Route pour obtenir un article spécifique
@router.get("/items/{item_id}", response_model=ItemSchema)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item_repository = ItemRepository(db)
    item = item_repository.read(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Route pour mettre à jour un article existant
@router.put("/items/{item_id}", response_model=ItemSchema)
def update_item(item_id: int, item: ItemSchema, db: Session = Depends(get_db)):
    item_repository = ItemRepository(db)
    updated_item = item_repository.update(Item(id=item_id, **item.dict()))
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


# Route pour supprimer un article
@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item_repository = ItemRepository(db)
    item_repository.delete(item_id)
    return {"message": "Item deleted"}



