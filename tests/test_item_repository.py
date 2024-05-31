import sys
import os

# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.item_model import Item
from repositories.item_repository import ItemRepository
from db.database import Base

# Configuration de la base de données pour les tests
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialisation de la base de données
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def db_session():
    """
    Fixture pour fournir une session de base de données pour les tests.
    """
    session = TestingSessionLocal()
    yield session
    session.close()

def test_create_item(db_session):
    """
    Test de la méthode create de ItemRepository.
    """
    repo = ItemRepository(db_session)
    item = Item(name="Test Item", description="This is a test item", price=10.0, is_available=True)
    created_item = repo.create(item)
    assert created_item.id is not None
    assert created_item.name == "Test Item"
    assert created_item.description == "This is a test item"
    assert created_item.price == 10.0
    assert created_item.is_available is True

def test_get_all_items(db_session):
    """
    Test de la méthode get_all de ItemRepository.
    """
    repo = ItemRepository(db_session)
    items = repo.get_all()
    assert len(items) == 1  # Nous avons ajouté un élément dans le test précédent

def test_read_item(db_session):
    """
    Test de la méthode read de ItemRepository.
    """
    repo = ItemRepository(db_session)
    item = repo.read(1)
    assert item is not None
    assert item.id == 1
    assert item.name == "Test Item"

def test_update_item(db_session):
    """
    Test de la méthode update de ItemRepository.
    """
    repo = ItemRepository(db_session)
    item = Item(id=1, name="Updated Item", description="This is an updated test item", price=20.0, is_available=False)
    updated_item = repo.update(item)
    assert updated_item is not None
    assert updated_item.name == "Updated Item"
    assert updated_item.description == "This is an updated test item"
    assert updated_item.price == 20.0
    assert updated_item.is_available is False

def test_delete_item(db_session):
    """
    Test de la méthode delete de ItemRepository.
    """
    repo = ItemRepository(db_session)
    repo.delete(1)
    item = repo.read(1)
    assert item is None
