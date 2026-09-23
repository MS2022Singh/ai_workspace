import sqlite3
import os

class BugEliminator:
    def __init__(self, db_path="workspace_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                details TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def inspect_system(self):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM system_logs")
            count = cursor.fetchone()[0]
            conn.close()
            return {"status": "clean", "total_logged_events": count, "active_issues": 0}
        except Exception as e:
            return {"status": "degraded", "error": str(e), "active_issues": 1}

bug_eliminator = BugEliminator()
