CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME NOT NULL
);

CREATE TABLE spellbook_memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_key TEXT NOT NULL,
    memory_value TEXT NOT NULL,
    priority INTEGER NOT NULL,
    embedding BLOB NOT NULL
);