import sqlite3
import os
from contextlib import contextmanager
from typing import Generator, Optional


class DbConnection:
    def __init__(self, db_path: str = "kairos.db"):
        self.db_path = db_path
        self.ensure_db_directory()

    def ensure_db_directory(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn: Optional[sqlite3.Connection] = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA journal_mode = WAL")

            yield conn

        except sqlite3.Error as e:
            print(f"Oh no! Error connecting to Database: {e}")
            raise
        except Exception as e:
            print(f"Oh no! Unexpected error: {e}")
            raise
        finally:
            if conn:
                conn.close()
