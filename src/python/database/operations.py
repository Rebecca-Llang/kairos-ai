import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any, Callable, TypeVar
from .connection import DbConnection

T = TypeVar("T")

# Small helpers
def _now_iso() -> str:
    return datetime.now().isoformat()

def _normalize_memory_key(key: str) -> str:
    return key.strip().lower()

def _with_conn(db_path: str, fn: Callable[[Any], T]) -> T:
    db_conn = DbConnection(db_path)
    with db_conn.get_connection() as conn:
        return fn(conn)

def init_db(db_path: str = "kairos.db", schema_path: str = "database/schema.sql") -> bool:
    try:
        if not os.path.exists(schema_path):
            print(f"Schema file not found at: {schema_path}")
            return False

        with open(schema_path, "r") as f:
            schema_sql = f.read()

        def _run(conn):
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = cursor.fetchall()
            if existing_tables:
                print(f"Database already initialised with {len(existing_tables)} tables.")
                return True
            conn.executescript(schema_sql)
            conn.commit()
            print("Database initialised successfully!")
            return True

        return _with_conn(db_path, _run)
    except Exception as e:
        print(f"Oh no! Error initializing database: {e}")
        return False
  
# CHAT HISTORY #

def add_chat_message(role: str, content: str, timestamp: Optional[str] = None, db_path: str = "kairos.db") -> Optional[int]:
    """Add a new chat message to the database. Returns inserted row id or None on error."""
    try:
        if role.lower() not in {"user", "assistant"}:
            raise ValueError("Role must be 'user' or 'assistant'")
        if not content.strip():
            raise ValueError("Content cannot be empty")
        if timestamp is None:
            timestamp = _now_iso()

        def _run(conn):
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_history (role, content, timestamp) VALUES (?, ?, ?)",
                (role, content, timestamp)
            )
            conn.commit()
            return int(cursor.lastrowid)

        return _with_conn(db_path, _run)
    except Exception as e:
        print(f"Error adding chat message: {e}")
        return None
      
def get_chat_history(limit: Optional[int] = None, db_path: str = "kairos.db") -> List[Dict[str, Any]]:
    """Get the chat history from the database as a list of dict rows."""
    try:
        def _run(conn):
            cursor = conn.cursor()
            if limit is not None:
                cursor.execute(
                    "SELECT id, role, content, timestamp FROM chat_history ORDER BY timestamp DESC LIMIT ?",
                    (limit,)
                )
            else:
                cursor.execute(
                    "SELECT id, role, content, timestamp FROM chat_history ORDER BY timestamp DESC"
                )
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

        return _with_conn(db_path, _run)
    except Exception as e:
        print(f"Error getting chat history: {e}")
        return []

def get_recent_chat_history(count: int = 10, db_path: str = "kairos.db") -> List[Dict[str, Any]]:
    """Get the most recent chat messages (default 10)."""
    return get_chat_history(limit=count, db_path=db_path)
  
def delete_chat_history(db_path: str = "kairos.db") -> bool:
  """Delete the chat history from the database."""
  try:
    def _run(conn):
      cursor = conn.cursor()
      cursor.execute("DELETE FROM chat_history")
      conn.commit()
      return True
    return _with_conn(db_path, _run)
  except Exception as e:
    print(f"Error deleting chat history: {e}")
    return False
    
def delete_chat_msg_by_id(msg_id: int, db_path: str = "kairos.db") -> int:
  """Delete a chat message by ID."""
  try:
    def _run(conn):
      cursor = conn.cursor()
      cursor.execute("DELETE FROM chat_history WHERE id = ?", (msg_id,))
      conn.commit()
      return int(cursor.rowcount)
    return _with_conn(db_path, _run)
  except Exception as e:
    print(f"Error deleting chat message by ID: {e}")
    return 0
  
# SPELLBOOK MEMORIES #

def add_memory(memory_key: str, memory_value: str, priority: int = 5, embedding: Optional[List[float]] = None, db_path: str = "kairos.db") -> Optional[int]:
    """Add or update a memory by memory_key. Returns id or None."""
    try:
        key = _normalize_memory_key(memory_key)
        if not key:
            raise ValueError("memory_key is required")
        if not memory_value.strip():
            raise ValueError("memory_value is required")
        # Clamp priority
        priority = max(1, min(10, priority))
        # Serialize embedding as JSON text (schema uses TEXT)
        embedding_text = json.dumps(embedding) if embedding is not None else None

        def _run(conn):
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO spellbook_memories (memory_key, memory_value, priority, embedding)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(memory_key) DO UPDATE SET
                    memory_value = excluded.memory_value,
                    priority     = excluded.priority,
                    embedding    = excluded.embedding,
                    updated_at   = CURRENT_TIMESTAMP
                """,
                (key, memory_value, priority, embedding_text)
            )
            conn.commit()
            if cursor.lastrowid:
                return int(cursor.lastrowid)
            cursor.execute("SELECT id FROM spellbook_memories WHERE memory_key = ?", (key,))
            row = cursor.fetchone()
            return int(row["id"]) if row else None

        return _with_conn(db_path, _run)
    except Exception as e:
        print(f"Error adding memory: {e}")
        return None
    
def get_memory_by_key(memory_key: str, db_path: str = "kairos.db") -> Optional[Dict[str, Any]]:
    """Get a specific memory by key as a dict."""
    try:
        key = _normalize_memory_key(memory_key)
        def _run(conn):
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, memory_key, memory_value, priority, embedding, created_at, updated_at FROM spellbook_memories WHERE memory_key = ?",
                (key,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            data = dict(row)
            # Deserialize embedding JSON text to Python object
            if data.get("embedding"):
                try:
                    data["embedding"] = json.loads(data["embedding"])  # type: ignore[arg-type]
                except Exception:
                    # If malformed, leave as-is
                    pass
            return data
        return _with_conn(db_path, _run)
    except Exception as e:
        print(f"Error getting memory by key: {e}")
        return None
    
def get_all_memories(db_path: str = "kairos.db") -> List[Dict[str, Any]]:
    """Get all memories from the spellbook as list of dicts."""
    try:
        def _run(conn):
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, memory_key, memory_value, priority, embedding, created_at, updated_at FROM spellbook_memories ORDER BY priority DESC, created_at DESC"
            )
            rows = cursor.fetchall()
            results: List[Dict[str, Any]] = []
            for r in rows:
                item = dict(r)
                if item.get("embedding"):
                    try:
                        item["embedding"] = json.loads(item["embedding"])  # type: ignore[arg-type]
                    except Exception:
                        pass
                results.append(item)
            return results
        return _with_conn(db_path, _run)
    except Exception as e:
        print(f"Error getting all memories: {e}")
        return []


def delete_memory_by_key(memory_key: str, db_path: str = "kairos.db") -> bool:
    """Delete a memory by key."""
    try:
        key = _normalize_memory_key(memory_key)
        def _run(conn):
            cursor = conn.cursor()
            cursor.execute("DELETE FROM spellbook_memories WHERE memory_key = ?", (key,))
            conn.commit()
            return True
        return _with_conn(db_path, _run)
    except Exception as e:
        print(f"Error deleting memory by key: {e}")
        return False

def delete_all_memories(db_path: str = "kairos.db") -> bool:
    """Delete all memories from the spellbook."""
    try:
        def _run(conn):
            cursor = conn.cursor()
            cursor.execute("DELETE FROM spellbook_memories")
            conn.commit()
            return True
        return _with_conn(db_path, _run)
    except Exception as e:
        print(f"Error deleting all memories: {e}")
        return False
    
# UTILITIES #

def get_database_stats(db_path: str = "kairos.db") -> Dict[str, Any]:
    """Get database statistics."""
    try:
        def _run(conn):
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM chat_history")
            chat_history_count = int(cursor.fetchone()[0])
            cursor.execute("SELECT COUNT(*) FROM spellbook_memories")
            spellbook_memories_count = int(cursor.fetchone()[0])
            return {
                "chat_history_count": chat_history_count,
                "spellbook_memories_count": spellbook_memories_count
            }
        return _with_conn(db_path, _run)
    except Exception as e:
        print(f"Error getting database statistics: {e}")
        return {}
    
def clear_chat_history(db_path: str = "kairos.db") -> bool:
    """Clear all chat history."""
    try:
        def _run(conn):
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_history")
            conn.commit()
            return True
        return _with_conn(db_path, _run)
    except Exception as e:
        print(f"Error clearing chat history: {e}")
        return False