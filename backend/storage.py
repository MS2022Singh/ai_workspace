"""
Local-only persistence layer. Everything lives in a single SQLite file on
disk on the user's machine (no network calls). Optional at-rest encryption
of task content is handled transparently via backend.security.
"""
import sqlite3
import json
import time
import threading
import shutil
import base64
from pathlib import Path
from . import security

APP_DIR = Path.home() / ".ai_workspace"
APP_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = APP_DIR / "workspace.db"
PROJECTS_DIR = APP_DIR / "projects"
PROJECTS_DIR.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()


def _conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _lock, _conn() as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'queued',
                result_summary TEXT,
                parent_task_id INTEGER,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS task_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS task_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS task_attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )
        try:
            c.execute("ALTER TABLE tasks ADD COLUMN parent_task_id INTEGER")
        except sqlite3.OperationalError:
            pass  # already migrated
        c.commit()


# ---------- settings ----------

DEFAULT_SETTINGS = {
    "concurrency": "2",
    "encryption_enabled": "false",
    "model_coordinator": "llama3.2:3b",
    "model_coder": "qwen2.5-coder:7b",
    "model_reviewer": "qwen2.5-coder:7b",
    "model_documenter": "llama3.2:3b",
    "model_proofreader": "llama3.2:3b",
    "model_researcher": "llama3.2:3b",
    "model_analyst": "llama3.2:3b",
    "model_economist": "llama3.2:3b",
    "model_writer": "llama3.2:3b",
    "model_historian": "llama3.2:3b",
    "model_archaeologist": "llama3.2:3b",
    "model_scientist": "llama3.2:3b",
    "model_engineer": "llama3.2:3b",
    "model_vision": "llava",
    "model_specialist": "llama3.2:3b",
    "lan_access_enabled": "false",
    "access_code": "",
    "web_research_enabled": "false",
}


def get_settings():
    with _lock, _conn() as c:
        rows = c.execute("SELECT key, value FROM settings").fetchall()
        s = dict(DEFAULT_SETTINGS)
        for r in rows:
            s[r["key"]] = r["value"]
    if not s.get("access_code"):
        s["access_code"] = security.generate_code()
        set_settings({"access_code": s["access_code"]})
    return s


def set_settings(updates: dict):
    with _lock, _conn() as c:
        for k, v in updates.items():
            c.execute(
                "INSERT INTO settings (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (k, str(v)),
            )
        c.commit()


# ---------- projects ----------

def create_project(name: str):
    with _lock, _conn() as c:
        cur = c.execute(
            "INSERT INTO projects (name, created_at) VALUES (?, ?)",
            (name, time.time()),
        )
        c.commit()
        pid = cur.lastrowid
    (PROJECTS_DIR / str(pid)).mkdir(parents=True, exist_ok=True)
    return pid


def list_projects():
    with _lock, _conn() as c:
        rows = c.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]


# ---------- tasks ----------

def create_task(project_id: int, description: str, attachments: list = None, parent_task_id: int = None):
    """
    attachments: optional list of {"filename": str, "text": str|None, "note": str|None}
    Stored atomically with the task row so the background scheduler never
    sees a task before its attachments are saved.
    """
    attachments = attachments or []
    enc = get_settings().get("encryption_enabled") == "true"
    stored_desc = security.encrypt(description) if enc else description
    with _lock, _conn() as c:
        cur = c.execute(
            "INSERT INTO tasks (project_id, description, status, parent_task_id, created_at, updated_at) "
            "VALUES (?, ?, 'queued', ?, ?, ?)",
            (project_id, stored_desc, parent_task_id, time.time(), time.time()),
        )
        tid = cur.lastrowid
        for a in attachments:
            content = a.get("text")
            if content is None:
                content = f"[Could not read contents of '{a['filename']}': {a.get('note') or 'unsupported file type'}. The team knows this file was attached but cannot see inside it.]"
            stored_content = security.encrypt(content) if enc else content
            c.execute(
                "INSERT INTO task_attachments (task_id, filename, content, created_at) VALUES (?, ?, ?, ?)",
                (tid, a["filename"], stored_content, time.time()),
            )
        c.commit()
        return tid


def _decrypt_field(value):
    if value is None:
        return value
    return security.decrypt(value)


def get_task(task_id: int):
    with _lock, _conn() as c:
        row = c.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not row:
            return None
        d = dict(row)
        d["description"] = _decrypt_field(d["description"])
        if d.get("result_summary"):
            d["result_summary"] = _decrypt_field(d["result_summary"])
        return d


def list_tasks(project_id: int):
    with _lock, _conn() as c:
        rows = c.execute(
            "SELECT * FROM tasks WHERE project_id=? ORDER BY created_at DESC", (project_id,)
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["description"] = _decrypt_field(d["description"])
            if d.get("result_summary"):
                d["result_summary"] = _decrypt_field(d["result_summary"])
            out.append(d)
        return out


def list_queued_tasks():
    with _lock, _conn() as c:
        rows = c.execute("SELECT id FROM tasks WHERE status='queued' ORDER BY created_at ASC").fetchall()
        return [r["id"] for r in rows]


def count_running_tasks():
    with _lock, _conn() as c:
        row = c.execute("SELECT COUNT(*) AS n FROM tasks WHERE status='running'").fetchone()
        return row["n"]


def update_task_description(task_id: int, description: str):
    enc = get_settings().get("encryption_enabled") == "true"
    stored = security.encrypt(description) if enc else description
    with _lock, _conn() as c:
        c.execute(
            "UPDATE tasks SET description=?, updated_at=? WHERE id=?",
            (stored, time.time(), task_id),
        )
        c.commit()


def delete_task(task_id: int):
    with _lock, _conn() as c:
        c.execute("DELETE FROM task_logs WHERE task_id=?", (task_id,))
        c.execute("DELETE FROM task_files WHERE task_id=?", (task_id,))
        c.execute("DELETE FROM task_attachments WHERE task_id=?", (task_id,))
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        c.commit()


def delete_project(project_id: int):
    with _lock, _conn() as c:
        task_ids = [r["id"] for r in c.execute("SELECT id FROM tasks WHERE project_id=?", (project_id,)).fetchall()]
        for tid in task_ids:
            c.execute("DELETE FROM task_logs WHERE task_id=?", (tid,))
            c.execute("DELETE FROM task_files WHERE task_id=?", (tid,))
            c.execute("DELETE FROM task_attachments WHERE task_id=?", (tid,))
        c.execute("DELETE FROM tasks WHERE project_id=?", (project_id,))
        c.execute("DELETE FROM projects WHERE id=?", (project_id,))
        c.commit()
    shutil.rmtree(PROJECTS_DIR / str(project_id), ignore_errors=True)


def update_task_status(task_id: int, status: str, result_summary: str = None):
    enc = get_settings().get("encryption_enabled") == "true"
    with _lock, _conn() as c:
        if result_summary is not None:
            stored = security.encrypt(result_summary) if enc else result_summary
            c.execute(
                "UPDATE tasks SET status=?, result_summary=?, updated_at=? WHERE id=?",
                (status, stored, time.time(), task_id),
            )
        else:
            c.execute(
                "UPDATE tasks SET status=?, updated_at=? WHERE id=?",
                (status, time.time(), task_id),
            )
        c.commit()


def add_log(task_id: int, role: str, message: str):
    enc = get_settings().get("encryption_enabled") == "true"
    stored = security.encrypt(message) if enc else message
    with _lock, _conn() as c:
        c.execute(
            "INSERT INTO task_logs (task_id, role, message, created_at) VALUES (?, ?, ?, ?)",
            (task_id, role, stored, time.time()),
        )
        c.commit()


def get_logs(task_id: int):
    with _lock, _conn() as c:
        rows = c.execute(
            "SELECT * FROM task_logs WHERE task_id=? ORDER BY created_at ASC", (task_id,)
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["message"] = _decrypt_field(d["message"])
            out.append(d)
        return out


def save_file(task_id: int, project_id: int, filename: str, content):
    """content may be str (plain text) or bytes (a native binary file like
    a generated .docx/.xlsx/.pptx)."""
    enc = get_settings().get("encryption_enabled") == "true"
    is_binary = isinstance(content, bytes)
    if is_binary:
        b64 = base64.b64encode(content).decode("ascii")
        stored = security.encrypt("BINARY_BASE64::" + b64) if enc else "BINARY_BASE64::" + b64
    else:
        stored = security.encrypt(content) if enc else content
    with _lock, _conn() as c:
        c.execute(
            "INSERT INTO task_files (task_id, filename, content, created_at) VALUES (?, ?, ?, ?)",
            (task_id, filename, stored, time.time()),
        )
        c.commit()
    # Also write a copy to disk in the project folder so the user can open
    # it directly in their editor/Word/Excel of choice.
    task_dir = PROJECTS_DIR / str(project_id) / f"task_{task_id}"
    task_dir.mkdir(parents=True, exist_ok=True)
    safe_name = filename.replace("..", "_").lstrip("/\\")
    target = task_dir / safe_name
    target.parent.mkdir(parents=True, exist_ok=True)
    if is_binary:
        target.write_bytes(content)
    else:
        target.write_text(content, encoding="utf-8")
    return str(target)


def get_attachments(task_id: int):
    with _lock, _conn() as c:
        rows = c.execute(
            "SELECT * FROM task_attachments WHERE task_id=? ORDER BY created_at ASC", (task_id,)
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["content"] = _decrypt_field(d["content"])
            out.append(d)
        return out


def get_files(task_id: int):
    """Returns file rows with `content` as str (text) or bytes (binary,
    e.g. a generated .docx/.xlsx/.pptx -- decoded back from storage)."""
    with _lock, _conn() as c:
        rows = c.execute(
            "SELECT * FROM task_files WHERE task_id=? ORDER BY created_at ASC", (task_id,)
        ).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            content = _decrypt_field(d["content"])
            if isinstance(content, str) and content.startswith("BINARY_BASE64::"):
                d["content"] = base64.b64decode(content[len("BINARY_BASE64::"):])
                d["is_binary"] = True
            else:
                d["content"] = content
                d["is_binary"] = False
            out.append(d)
        return out
