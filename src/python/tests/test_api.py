#!/usr/bin/env python3
"""
Essential API Integration Tests - Core database operations
"""
import unittest
import os
import sys

# Add the src/python directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.operations import (
    init_db, add_chat_message, get_chat_history, add_memory, 
    get_all_memories, delete_memory_by_key, get_database_stats
)

class TestAPIIntegration(unittest.TestCase):
    """Test essential API integration with database operations."""
    
    def setUp(self):
        """Set up test database."""
        self.test_db_path = "test_api.db"
        self.schema_path = os.path.join(os.path.dirname(__file__), "..", "database", "schema.sql")
        
        # Initialize test database
        init_db(self.test_db_path, self.schema_path)
    
    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def test_chat_message_flow(self):
        """Test the complete chat message flow."""
        # Add user message
        user_msg_id = add_chat_message(
            "user", 
            "Hello Kairos!", 
            db_path=self.test_db_path
        )
        self.assertIsNotNone(user_msg_id)
        
        # Add AI response
        ai_msg_id = add_chat_message(
            "assistant", 
            "Hello! How can I help you today?", 
            db_path=self.test_db_path
        )
        self.assertIsNotNone(ai_msg_id)
        
        # Get chat history
        history = get_chat_history(db_path=self.test_db_path)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['role'], 'assistant')  # Most recent first
        self.assertEqual(history[1]['role'], 'user')
    
    def test_memory_operations(self):
        """Test memory CRUD operations."""
        # Add memory
        memory_id = add_memory(
            "test_key",
            "Test memory value",
            8,
            db_path=self.test_db_path
        )
        self.assertIsNotNone(memory_id)
        
        # Get all memories
        memories = get_all_memories(db_path=self.test_db_path)
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0]['memory_key'], 'test_key')
        self.assertEqual(memories[0]['memory_value'], 'Test memory value')
        self.assertEqual(memories[0]['priority'], 8)
        
        # Delete memory
        success = delete_memory_by_key('test_key', db_path=self.test_db_path)
        self.assertTrue(success)
        
        # Verify deletion
        memories = get_all_memories(db_path=self.test_db_path)
        self.assertEqual(len(memories), 0)
    
    def test_database_stats(self):
        """Test database statistics."""
        # Add some test data
        add_chat_message("user", "Test message 1", db_path=self.test_db_path)
        add_chat_message("assistant", "Test response 1", db_path=self.test_db_path)
        add_memory("key1", "value1", 5, db_path=self.test_db_path)
        add_memory("key2", "value2", 7, db_path=self.test_db_path)
        
        # Get stats
        stats = get_database_stats(db_path=self.test_db_path)
        self.assertEqual(stats['chat_history_count'], 2)
        self.assertEqual(stats['spellbook_memories_count'], 2)


if __name__ == '__main__':
    unittest.main()
