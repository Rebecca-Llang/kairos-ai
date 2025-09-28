#!/usr/bin/env python3
"""
Database integration tests for Kairos AI.
Tests core database functionality with temporary databases.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.operations import (
    init_db, add_chat_message, get_chat_history, add_memory, 
    get_all_memories, get_database_stats, clear_chat_history,
    delete_memory_by_key
)


class TestDatabaseIntegration(unittest.TestCase):
    """Test database integration functionality."""
    
    def setUp(self):
        """Set up test database."""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
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
        self.assertEqual(stats['chat_history_count'], 0)
        self.assertEqual(stats['spellbook_memories_count'], 0)
    
    def test_chat_message_crud(self):
        """Test chat message operations."""
        # Add messages
        msg_id1 = add_chat_message("user", "Hello Kairos!", db_path=self.db_path)
        msg_id2 = add_chat_message("assistant", "Hello! How can I help?", db_path=self.db_path)
        
        self.assertIsNotNone(msg_id1)
        self.assertIsNotNone(msg_id2)
        
        # Retrieve history
        history = get_chat_history(db_path=self.db_path)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['role'], 'assistant')  # Most recent first
        self.assertEqual(history[1]['role'], 'user')
        
        # Clear history
        self.assertTrue(clear_chat_history(self.db_path))
        history = get_chat_history(db_path=self.db_path)
        self.assertEqual(len(history), 0)
    
    def test_memory_crud(self):
        """Test memory operations."""
        # Add memory
        memory_id = add_memory(
            memory_key="favorite_coffee",
            memory_value="oat milk flat white",
            priority=8,
            embedding=[0.1, 0.2, 0.3],
            db_path=self.db_path
        )
        self.assertIsNotNone(memory_id)
        
        # Retrieve memories
        memories = get_all_memories(self.db_path)
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0]['memory_key'], 'favorite_coffee')
        self.assertEqual(memories[0]['priority'], 8)
        
        # Test upsert (update existing)
        add_memory(
            memory_key="favorite_coffee",
            memory_value="soy milk cappuccino",
            priority=9,
            db_path=self.db_path
        )
        
        memories = get_all_memories(self.db_path)
        self.assertEqual(len(memories), 1)  # Still only one
        self.assertEqual(memories[0]['memory_value'], 'soy milk cappuccino')
        self.assertEqual(memories[0]['priority'], 9)
        
        # Delete memory
        self.assertTrue(delete_memory_by_key("favorite_coffee", self.db_path))
        memories = get_all_memories(self.db_path)
        self.assertEqual(len(memories), 0)
    
    def test_database_stats(self):
        """Test database statistics."""
        # Add data
        add_chat_message("user", "Hello", db_path=self.db_path)
        add_chat_message("assistant", "Hi!", db_path=self.db_path)
        add_memory("test_key", "test_value", priority=7, db_path=self.db_path)
        
        # Check stats
        stats = get_database_stats(self.db_path)
        self.assertEqual(stats['chat_history_count'], 2)
        self.assertEqual(stats['spellbook_memories_count'], 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
