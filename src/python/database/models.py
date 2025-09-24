# This file defines data models for chat messages and spellbook memories.
# It includes type-safe dataclasses, validation, normalization helpers,
# and utilities to convert to/from database rows and plain dicts.

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Iterable
from datetime import datetime


def now_iso() -> str:
    return datetime.now().isoformat()


def normalize_memory_key(key: str) -> str:
    return key.strip().lower()


# Canonical memory keys supported by the app. Custom keys are allowed too.
MEMORY_KEYS: List[str] = [
    "name",
    "preferred_name",
    "pronouns",
    "neurodivergence",
    "personal_challenges",
    "personal_strengths",
    "current_goals",
    "productivity_methods_that_work",
    "productivity_methods_that_failed",
    "communication_preference",
    "energy_pattern",
    "emotional_regulation_tools",
    "likes",
    "dislikes",
    "values",
]


@dataclass
class ChatMessage:
    id: Optional[int] = None
    role: str = ""
    content: str = ""
    timestamp: str = field(default_factory=now_iso)

    def validate(self) -> bool:
        return self.role.lower() in {"user", "assistant"} and bool(self.content.strip())

    @staticmethod
    def from_row(row: Any) -> "ChatMessage":
        # row can be sqlite3.Row or dict
        r: Dict[str, Any] = dict(row)
        return ChatMessage(
            id=r.get("id"),
            role=r.get("role", ""),
            content=r.get("content", ""),
            timestamp=r.get("timestamp") or now_iso(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SpellbookMemory:
    id: Optional[int] = None
    memory_key: str = ""
    memory_value: str = ""
    priority: int = 5
    embedding: Optional[List[float]] = None  # Stored as JSON TEXT in DB
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def normalize(self) -> None:
        if self.memory_key:
            self.memory_key = normalize_memory_key(self.memory_key)
        # Clamp priority
        if self.priority is None:
            self.priority = 5
        self.priority = max(1, min(10, int(self.priority)))

    def validate(self) -> bool:
        if not self.memory_key or not self.memory_value.strip():
            return False
        return 1 <= self.priority <= 10

    @staticmethod
    def from_row(row: Any) -> "SpellbookMemory":
        r: Dict[str, Any] = dict(row)
        return SpellbookMemory(
            id=r.get("id"),
            memory_key=r.get("memory_key", ""),
            memory_value=r.get("memory_value", ""),
            priority=r.get("priority", 5),
            embedding=r.get("embedding"),  # JSON string will be deserialized by ops layer
            created_at=r.get("created_at"),
            updated_at=r.get("updated_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

