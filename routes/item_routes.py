from fastapi import APIRouter, Depends, HTTPException, Query
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


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db  # initialiser la session de base de données

    # Méthode pour obtenir tous les articles, avec pagination
    def get_all(self, skip: int = 0, limit: int = 10):
        return self.db.query(Item).offset(skip).limit(limit).all()

    # Méthode pour créer un nouvel article
    def create(self, item: Item) -> Item:
        self.db.add(item)  # ajouter l'article à la base de données
        self.db.commit()  # confirmer la transaction
        self.db.refresh(item)  # rafraichir l'article avec les données actuelles de la base de données
        return item  # renvoyer l'article créé

    # Méthode pour lire (obtenir) un article par son identifiant
    def read(self, item_id: int) -> Item:
        return self.db.query(Item).filter(Item.id == item_id).first()

    # Méthode pour mettre à jour un article existant
    def update(self, item: Item) -> Item:
        db_item = self.db.query(Item).filter(Item.id == item.id).first()
        if db_item:
            db_item.name = item.name
            db_item.description = item.description
            db_item.price = item.price
            db_item.is_available = item.is_available
            self.db.commit()  # confirmer la transaction
            self.db.refresh(db_item)  # rafraichir l'article avec les données actuelles de la base de données
            return db_item  # renvoyer l'article mis à jour

    # Méthode pour supprimer un article
    def delete(self, item_id: int) -> None:
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if item:
            self.db.delete(item)  # supprimer l'élément de la base de données
            self.db.commit()  # confirmer la transaction
