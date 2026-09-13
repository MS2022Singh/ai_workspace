import sqlite3
import os

class MemoryEngine:
    def __init__(self, db_path='workspace_memory.db'):
        self.db_path = db_path
        # For :memory:, keep a persistent connection to prevent data loss across calls
        if self.db_path == ':memory:':
            self._conn = sqlite3.connect(':memory:', check_same_thread=False)
        else:
            self._conn = None
        self.init_db()

    def get_connection(self):
        if self._conn:
            return self._conn
        return sqlite3.connect(self.db_path)

    def init_db(self):
        conn = self.get_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                key TEXT PRIMARY KEY,
                value TEXT,
                category TEXT
            )
        ''')
        conn.commit()
        if not self._conn:
            conn.close()

    def set_memory(self, key: str, value: str, category: str = 'general'):
        conn = self.get_connection()
        conn.execute('''
            INSERT OR REPLACE INTO memory (key, value, category)
            VALUES (?, ?, ?)
        ''', (key, value, category))
        conn.commit()
        if not self._conn:
            conn.close()

    def get_memory(self, key: str):
        conn = self.get_connection()
        cursor = conn.execute('SELECT value FROM memory WHERE key = ?', (key,))
        row = cursor.fetchone()
        if not self._conn:
            conn.close()
        return row[0] if row else None
