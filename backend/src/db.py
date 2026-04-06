"""SQLite cache for processed analytics — avoids re-aggregating on every request."""

import sqlite3
from pathlib import Path

_DB_PATH = Path(__file__).parent.parent / "analytics_cache.db"
_conn: sqlite3.Connection | None = None


def get_db() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _init_tables(_conn)
    return _conn


def _init_tables(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS statements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            actor_email TEXT NOT NULL,
            actor_name TEXT,
            verb TEXT NOT NULL,
            activity_id TEXT NOT NULL,
            activity_name TEXT,
            score REAL,
            completion INTEGER,
            duration_minutes REAL,
            timestamp TEXT NOT NULL,
            raw_json TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_stmt_actor ON statements(actor_email);
        CREATE INDEX IF NOT EXISTS idx_stmt_verb ON statements(verb);
        CREATE INDEX IF NOT EXISTS idx_stmt_activity ON statements(activity_id);
        CREATE INDEX IF NOT EXISTS idx_stmt_ts ON statements(timestamp);

        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        );
    """)
    conn.commit()


def insert_statements(statements: list[dict]):
    conn = get_db()
    conn.executemany(
        """INSERT INTO statements
           (actor_email, actor_name, verb, activity_id, activity_name,
            score, completion, duration_minutes, timestamp, raw_json)
           VALUES (:actor_email, :actor_name, :verb, :activity_id, :activity_name,
                   :score, :completion, :duration_minutes, :timestamp, :raw_json)""",
        statements,
    )
    conn.commit()


def clear_statements():
    conn = get_db()
    conn.execute("DELETE FROM statements")
    conn.commit()


def get_all_statements() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT * FROM statements ORDER BY timestamp").fetchall()
    return [dict(r) for r in rows]


def get_statement_count() -> int:
    conn = get_db()
    row = conn.execute("SELECT COUNT(*) as cnt FROM statements").fetchone()
    return row["cnt"]


def set_metadata(key: str, value: str):
    conn = get_db()
    conn.execute(
        "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
        (key, value),
    )
    conn.commit()


def get_metadata(key: str) -> str | None:
    conn = get_db()
    row = conn.execute("SELECT value FROM metadata WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else None


def close_db():
    global _conn
    if _conn:
        _conn.close()
        _conn = None
