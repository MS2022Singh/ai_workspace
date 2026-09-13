import sqlite3
import os

class MemoryEngine:
    def __init__(self, db_path='workspace_memory.db'):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS memory (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    category TEXT
                )
            ''')
            conn.commit()

    def set_memory(self, key: str, value: str, category: str = 'general'):
        with self.get_connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO memory (key, value, category)
                VALUES (?, ?, ?)
            ''', (key, value, category))
            conn.commit()

    def get_memory(self, key: str):
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT value FROM memory WHERE key = ?', (key,))
            row = cursor.fetchone()
            return row[0] if row else None
