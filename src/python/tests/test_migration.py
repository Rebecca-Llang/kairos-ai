#!/usr/bin/env python3
"""
Tests for the JSON to SQLite migration functionality.
"""

import os
import sys
import tempfile
import unittest
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from migrations.migrate_json_to_sqlite import MigrationConfig
from database.operations import get_database_stats, get_chat_history, get_all_memories


class TestMigration(unittest.TestCase):
    """Test migration functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        
        # Create data/templates directory structure
        templates_dir = self.temp_path / "data" / "templates"
        templates_dir.mkdir(parents=True)
        
        # Create test JSON files
        self.create_test_json_files(templates_dir)
        
        # Create migration config
        self.config = MigrationConfig(str(self.temp_path))
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_json_files(self, templates_dir):
        """Create test JSON files."""
        # Test chat history
        chat_history = [
            {"role": "user", "content": "Hello Kairos!", "timestamp": "2025-01-01T10:00:00"},
            {"role": "assistant", "content": "Hello! How can I help?", "timestamp": "2025-01-01T10:01:00"}
        ]
        
        # Test spellbook
        spellbook = [
            {
                "name": {"value": "Test User", "priority": 8, "embedding": [0.1, 0.2]},
                "coffee": {"value": "black coffee", "priority": 5, "embedding": [0.3, 0.4]}
            }
        ]
        
        # Write test files
        with open(templates_dir / "chat-history.json", "w") as f:
            json.dump(chat_history, f)
        
        with open(templates_dir / "the-spellbook-bee.json", "w") as f:
            json.dump(spellbook, f)
    
    def test_migration_config_initialization(self):
        """Test migration config setup."""
        self.assertEqual(self.config.base_path, self.temp_path)
        self.assertTrue(self.config.files['chat_history'].exists())
        self.assertTrue(self.config.files['spellbook_bee'].exists())
    
    def test_migration_process(self):
        """Test the complete migration process."""
        # Run migration
        success = self.config.run_migration(create_backup=False)
        self.assertTrue(success)
        
        # Verify database was created
        self.assertTrue(self.config.db_path.exists())
        
        # Verify data was migrated
        stats = get_database_stats(str(self.config.db_path))
        self.assertEqual(stats['chat_history_count'], 2)
        self.assertEqual(stats['spellbook_memories_count'], 2)
        
        # Verify chat history
        history = get_chat_history(db_path=str(self.config.db_path))
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['content'], 'Hello! How can I help?')
        self.assertEqual(history[1]['content'], 'Hello Kairos!')
        
        # Verify memories
        memories = get_all_memories(db_path=str(self.config.db_path))
        self.assertEqual(len(memories), 2)
        memory_keys = [m['memory_key'] for m in memories]
        self.assertIn('name', memory_keys)
        self.assertIn('coffee', memory_keys)


if __name__ == '__main__':
    unittest.main(verbosity=2)
