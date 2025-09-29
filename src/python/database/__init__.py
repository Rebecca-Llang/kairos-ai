# Database directory as a Python package
from .connection import DbConnection
from .models import ChatMessage, SpellbookMemory, MEMORY_KEYS
from .operations import (
    init_db,
    add_chat_message,
    get_chat_history,
    get_recent_chat_history,
    delete_chat_history,
    delete_chat_msg_by_id,
    add_memory,
    get_memory_by_key,
    get_all_memories,
    delete_memory_by_key,
    delete_all_memories,
    get_database_stats,
    clear_chat_history,
)

__all__ = [
    "DbConnection",
    "ChatMessage",
    "SpellbookMemory",
    "MEMORY_KEYS",
    "init_db",
    "add_chat_message",
    "get_chat_history",
    "get_recent_chat_history",
    "delete_chat_history",
    "delete_chat_msg_by_id",
    "add_memory",
    "get_memory_by_key",
    "get_all_memories",
    "delete_memory_by_key",
    "delete_all_memories",
    "get_database_stats",
    "clear_chat_history",
]
