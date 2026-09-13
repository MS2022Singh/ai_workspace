import sqlite3
import json
import time
import os

class MemoryManager:
    def __init__(self, db_path="data/workspace_memory.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS structured_memory (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodic_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                data TEXT,
                timestamp REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_memory (
                project_name TEXT PRIMARY KEY,
                state TEXT,
                updated_at REAL
            )
        """)
        conn.commit()
        conn.close()

    def set_fact(self, key: str, value: dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO structured_memory (key, value, updated_at) VALUES (?, ?, ?)",
            (key, json.dumps(value), time.time())
        )
        conn.commit()
        conn.close()

    def get_fact(self, key: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM structured_memory WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        return json.loads(row[0]) if row else None

    def log_episode(self, topic: str, data: dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO episodic_events (topic, data, timestamp) VALUES (?, ?, ?)",
            (topic, json.dumps(data), time.time())
        )
        conn.commit()
        conn.close()