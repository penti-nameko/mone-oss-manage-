import unittest
from database.db_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_manager = DatabaseManager()

    def test_connection(self):
        self.assertTrue(self.db_manager.connect(), "Database connection should be successful")

    def test_create_record(self):
        record = {'name': 'Test', 'value': 123}
        result = self.db_manager.create_record(record)
        self.assertTrue(result, "Record creation should be successful")

    def test_read_record(self):
        record_id = 1
        record = self.db_manager.read_record(record_id)
        self.assertIsNotNone(record, "Record should be found")

    def test_update_record(self):
        record_id = 1
        updated_data = {'name': 'Updated Test', 'value': 456}
        result = self.db_manager.update_record(record_id, updated_data)
        self.assertTrue(result, "Record update should be successful")

    def test_delete_record(self):
        record_id = 1
        result = self.db_manager.delete_record(record_id)
        self.assertTrue(result, "Record deletion should be successful")

if __name__ == '__main__':
    unittest.main()