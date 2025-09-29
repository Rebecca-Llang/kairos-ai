#!/usr/bin/env python3
"""
Core Database Operations Tests - Essential functionality only
"""
import os
import tempfile
import unittest
from pathlib import Path

from database.operations import (
    init_db,
    add_chat_message,
    get_chat_history,
    add_memory,
    get_all_memories,
    delete_memory_by_key,
    get_database_stats,
    clear_chat_history,
    get_memory_by_key,
)


class TestCoreOperations(unittest.TestCase):
    """Test core database operations - the essential functionality."""

    def setUp(self):
        """Set up test database."""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name

        # Get schema path
        schema_path = Path(__file__).parent.parent / "database" / "schema.sql"

        # Initialize database
        self.assertTrue(init_db(self.db_path, str(schema_path)))

    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_database_initialization(self):
        """Test database starts empty."""
        stats = get_database_stats(self.db_path)
        self.assertEqual(stats["chat_history_count"], 0)
        self.assertEqual(stats["spellbook_memories_count"], 0)

    def test_chat_message_flow(self):
        """Test complete chat message flow."""
        # Add user message
        user_msg_id = add_chat_message("user", "Hello Kairos!", db_path=self.db_path)
        self.assertIsNotNone(user_msg_id)

        # Add AI response
        ai_msg_id = add_chat_message(
            "assistant", "Hello! How can I help you today?", db_path=self.db_path
        )
        self.assertIsNotNone(ai_msg_id)

        # Get chat history
        history = get_chat_history(db_path=self.db_path)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "assistant")  # Most recent first
        self.assertEqual(history[1]["role"], "user")

        # Clear history
        self.assertTrue(clear_chat_history(self.db_path))
        history = get_chat_history(db_path=self.db_path)
        self.assertEqual(len(history), 0)

    def test_memory_operations(self):
        """Test memory CRUD operations."""
        # Add memory
        memory_id = add_memory(
            "favorite_coffee", "oat milk flat white", 8, db_path=self.db_path
        )
        self.assertIsNotNone(memory_id)

        # Get all memories
        memories = get_all_memories(db_path=self.db_path)
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0]["memory_key"], "favorite_coffee")
        self.assertEqual(memories[0]["memory_value"], "oat milk flat white")
        self.assertEqual(memories[0]["priority"], 8)

        # Get specific memory
        memory = get_memory_by_key("favorite_coffee", db_path=self.db_path)
        self.assertIsNotNone(memory)
        self.assertEqual(memory["memory_value"], "oat milk flat white")

        # Test upsert (update existing)
        add_memory("favorite_coffee", "soy milk cappuccino", 9, db_path=self.db_path)

        memories = get_all_memories(db_path=self.db_path)
        self.assertEqual(len(memories), 1)  # Still only one
        self.assertEqual(memories[0]["memory_value"], "soy milk cappuccino")
        self.assertEqual(memories[0]["priority"], 9)

        # Delete memory
        success = delete_memory_by_key("favorite_coffee", db_path=self.db_path)
        self.assertTrue(success)

        # Verify deletion
        memories = get_all_memories(db_path=self.db_path)
        self.assertEqual(len(memories), 0)

    def test_database_stats(self):
        """Test database statistics."""
        # Add some test data
        add_chat_message("user", "Test message 1", db_path=self.db_path)
        add_chat_message("assistant", "Test response 1", db_path=self.db_path)
        add_memory("key1", "value1", 5, db_path=self.db_path)
        add_memory("key2", "value2", 7, db_path=self.db_path)

        # Get stats
        stats = get_database_stats(db_path=self.db_path)
        self.assertEqual(stats["chat_history_count"], 2)
        self.assertEqual(stats["spellbook_memories_count"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
