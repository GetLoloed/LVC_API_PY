import unittest
import sqlite3
import os


class TestDatabaseCreation(unittest.TestCase):

    def test_database_creation(self):
        db_path = 'items.db'
        conn = None
        try:
            conn = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
        self.assertTrue(os.path.exists(db_path))


if __name__ == '__main__':
    unittest.main()
