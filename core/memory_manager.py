# core/memory_manager.py
import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "core/memory_store.db"

class MemoryManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()
        self.working_memory = {
            "current_objective": None,
            "current_files": [],
            "current_errors": [],
            "current_decisions": [],
            "agent_state": "IDLE"
        }

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semantic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT NOT NULL,
                category TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                details TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preference_memory (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def update_working_memory(self, key, value):
        self.working_memory[key] = value

    def get_working_memory(self):
        return self.working_memory

    def add_semantic_fact(self, fact, category="general"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO semantic_memory (fact, category) VALUES (?, ?)", (fact, category))
        conn.commit()
        conn.close()

    def log_episode(self, event_type, details):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO episodic_memory (event_type, details) VALUES (?, ?)", (event_type, json.dumps(details)))
        conn.commit()
        conn.close()

    def set_preference(self, key, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO preference_memory (key, value) VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()

    def get_preference(self, key):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM preference_memory WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

memory = MemoryManager()
