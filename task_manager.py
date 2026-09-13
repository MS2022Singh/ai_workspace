from memory_engine import MemoryEngine
from event_bus import EventBus

class TaskManager:
    def __init__(self, memory_engine: MemoryEngine, event_bus: EventBus):
        self.memory = memory_engine
        self.bus = event_bus
        self._init_table()

    def _init_table(self):
        conn = self.memory.get_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                title TEXT,
                status TEXT,
                assignee TEXT
            )
        ''')
        conn.commit()
        if not self.memory._conn:
            conn.close()

    def create_task(self, task_id: str, title: str, assignee: str = 'AI Expert'):
        conn = self.memory.get_connection()
        conn.execute('''
            INSERT OR REPLACE INTO tasks (task_id, title, status, assignee)
            VALUES (?, ?, ?, ?)
        ''', (task_id, title, 'PENDING', assignee))
        conn.commit()
        if not self.memory._conn:
            conn.close()
        self.bus.publish('TASK_CREATED', {'task_id': task_id, 'title': title})

    def get_task(self, task_id: str):
        conn = self.memory.get_connection()
        cursor = conn.execute('SELECT task_id, title, status, assignee FROM tasks WHERE task_id = ?', (task_id,))
        row = cursor.fetchone()
        if not self.memory._conn:
            conn.close()
        if row:
            return {'task_id': row[0], 'title': row[1], 'status': row[2], 'assignee': row[3]}
        return None
