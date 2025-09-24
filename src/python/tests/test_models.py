"""
Simple tests for database models: ChatMessage and SpellbookMemory.
Uses only stdlib unittest and temporary objects (no DB IO here).
"""
import unittest
from typing import Any

from database.models import ChatMessage, SpellbookMemory, normalize_memory_key


class TestModels(unittest.TestCase):
    def test_chat_message_validation_and_defaults(self):
        msg = ChatMessage(role="user", content="hello")
        self.assertTrue(msg.validate())
        self.assertIn("T", msg.timestamp)  # ISO-ish string

        bad = ChatMessage(role="admin", content="hi")
        self.assertFalse(bad.validate())

        empty = ChatMessage(role="assistant", content="   ")
        self.assertFalse(empty.validate())

    def test_chat_message_from_row(self):
        row: dict[str, Any] = {"id": 1, "role": "assistant", "content": "ok", "timestamp": "2025-01-01T00:00:00"}
        msg = ChatMessage.from_row(row)
        self.assertEqual(msg.id, 1)
        self.assertEqual(msg.role, "assistant")
        self.assertEqual(msg.content, "ok")
        self.assertEqual(msg.timestamp, "2025-01-01T00:00:00")

    def test_spellbook_memory_normalize_and_validate(self):
        mem = SpellbookMemory(memory_key="  Name  ", memory_value="Bee", priority=12)
        mem.normalize()
        self.assertEqual(mem.memory_key, "name")
        self.assertEqual(mem.priority, 10)  # clamped
        self.assertTrue(mem.validate())

        bad = SpellbookMemory(memory_key=" ", memory_value=" ", priority=0)
        bad.normalize()
        self.assertFalse(bad.validate())

    def test_spellbook_memory_from_row(self):
        row: dict[str, Any] = {
            "id": 3,
            "memory_key": "pronouns",
            "memory_value": "she/they",
            "priority": 8,
            "embedding": None,
            "created_at": "2025-01-01T00:00:00",
            "updated_at": "2025-01-01T00:01:00",
        }
        mem = SpellbookMemory.from_row(row)
        self.assertEqual(mem.id, 3)
        self.assertEqual(mem.memory_key, "pronouns")
        self.assertEqual(mem.memory_value, "she/they")
        self.assertEqual(mem.priority, 8)
        self.assertIsNone(mem.embedding)
        self.assertEqual(mem.created_at, "2025-01-01T00:00:00")
        self.assertEqual(mem.updated_at, "2025-01-01T00:01:00")

    def test_normalize_memory_key_helper(self):
        self.assertEqual(normalize_memory_key("  Preferred_Name  "), "preferred_name")


if __name__ == "__main__":
    unittest.main()


