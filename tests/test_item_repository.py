import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from repositories.item_repository import ItemRepository


class Item:
    def __init__(self, id=None, name=None, description=None, price=None, is_available=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.is_available = is_available


class TestItemRepository(unittest.TestCase):

    def setUp(self):

        self.db = MagicMock(spec=Session)
        self.item = Item(1, 'item1', 'description1', 10.0, True)
        self.item_repo = ItemRepository(self.db)

    def test_get_all(self):
        self.item_repo.get_all()
        self.db.query.assert_called_once_with(Item)
        self.db.query().all.assert_called_once()

    def test_create(self):
        self.item_repo.create(self.item)
        self.db.add.assert_called_once_with(self.item)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(self.item)

    def test_read(self):
        self.item_repo.read(1)
        self.db.query.assert_called_once_with(Item)
        self.db.query().filter.assert_called_once_with(Item.id == 1)
        self.db.query().filter().first.assert_called_once()

    def test_update(self):
        new_item = Item(1, 'item2', 'description2', 20.0, False)
        self.db.query().filter().first.return_value = self.item
        self.item_repo.update(new_item)
        assert self.item == new_item
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(self.item)

    def test_delete(self):
        self.db.query().filter().first.return_value = self.item
        self.item_repo.delete(1)
        self.db.delete.assert_called_once_with(self.item)
        self.db.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()