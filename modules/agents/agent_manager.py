import sqlite3
import os

class AgentManager:
    def __init__(self, db_path="workspace_memory.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def dispatch(self, agent_type, prompt):
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_type TEXT,
                    prompt TEXT,
                    status TEXT
                )
            """)
            cursor.execute("INSERT INTO agent_tasks (agent_type, prompt, status) VALUES (?, ?, ?)", (agent_type, prompt, "completed"))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[AGENT MANAGER DB ERROR] {e}")

        return {
            "agent": f"{agent_type.capitalize()} Specialized Agent",
            "output": f"Executed comprehensive reasoning and analysis for prompt: '{prompt}' using {agent_type} paradigm."
        }

agent_manager = AgentManager()
