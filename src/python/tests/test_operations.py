"""
Integration tests for database operations.
"""
import os
import tempfile
import unittest
from typing import Any

from database.operations import (
    init_db,
    add_chat_message,
    get_chat_history,
    add_memory,
    get_memory_by_key,
    clear_chat_history,
    delete_memory_by_key,
)


class TestOperations(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.tmp_db.name
        self.tmp_db.close()

        schema_path = os.path.join(os.path.dirname(__file__), "..", "database", "schema.sql")
        schema_path = os.path.abspath(schema_path)
        ok = init_db(self.db_path, schema_path)
        self.assertTrue(ok)

    def tearDown(self) -> None:
        try:
            os.remove(self.db_path)
        except Exception:
            pass

    def test_chat_flow(self):
        mid = add_chat_message("user", "hello", db_path=self.db_path)
        self.assertIsInstance(mid, int)
        history = get_chat_history(5, db_path=self.db_path)
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[0]["role"], "user")

        self.assertTrue(clear_chat_history(db_path=self.db_path))
        history2 = get_chat_history(5, db_path=self.db_path)
        self.assertEqual(len(history2), 0)

    def test_memory_flow(self):
        mem_id = add_memory("name", "Rebecca", 8, [0.1, 0.2], db_path=self.db_path)
        self.assertIsInstance(mem_id, int)

        rec = get_memory_by_key("name", db_path=self.db_path)
        self.assertIsNotNone(rec)
        self.assertEqual(rec["memory_value"], "Rebecca")
        self.assertEqual(rec["priority"], 8)
        self.assertEqual(rec["embedding"], [0.1, 0.2])

        self.assertTrue(delete_memory_by_key("name", db_path=self.db_path))
        rec2 = get_memory_by_key("name", db_path=self.db_path)
        self.assertIsNone(rec2)


if __name__ == "__main__":
    unittest.main()


