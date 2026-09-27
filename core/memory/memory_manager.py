import sqlite3
import os

class MemoryManager:
    def __init__(self, db_path="docs/project_memory/workspace_memory.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS project_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE,
                    value TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS episodic_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def set_fact(self, key: str, value: str):
        with self.conn:
            self.conn.execute('''
                INSERT INTO project_memory (key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP
            ''', (key, value))

    def log_episode(self, event_type: str, details: str):
        with self.conn:
            self.conn.execute('''
                INSERT INTO episodic_memory (event_type, details) VALUES (?, ?)
            ''', (event_type, details))

memory_manager = MemoryManager()
