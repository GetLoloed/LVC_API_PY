"""
Module de gestion des routes pour les articles.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from repositories.item_repository import ItemRepository
from models.item_model import Item
from schemas.item_schema import ItemSchema
from db.database import SessionLocal

router = APIRouter()


def get_db():
    """
    Définition de la dépendance pour obtenir la base de données.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/items/", response_model=List[ItemSchema])
def get_all_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Route pour obtenir tous les articles.
    """
    item_repository = ItemRepository(db)
    items = item_repository.get_all(skip=skip, limit=limit)
    return items


@router.post("/items/", response_model=ItemSchema)
def create_item(item: ItemSchema = Body(...), db: Session = Depends(get_db)):
    """
    Route pour créer un nouvel article.
    """
    item_repository = ItemRepository(db)
    created_item = item_repository.create(Item(**item.dict()))
    return created_item


@router.get("/items/{item_id}", response_model=ItemSchema)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Route pour obtenir un article spécifique.
    """
    item_repository = ItemRepository(db)
    item = item_repository.read(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/items/{item_id}", response_model=ItemSchema)
def update_item(item_id: int, item: ItemSchema, db: Session = Depends(get_db)):
    """
    Route pour mettre à jour un article existant.
    """
    item_repository = ItemRepository(db)
    updated_item = item_repository.update(Item(id=item_id, **item.dict()))
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Route pour supprimer un article.
    """
    item_repository = ItemRepository(db)
    item_repository.delete(item_id)
    return {"message": "Item deleted"}
