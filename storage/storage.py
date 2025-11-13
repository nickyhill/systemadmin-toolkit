import sqlite3
import json
import threading
from pathlib import Path

class Storage:
    _lock = threading.Lock()

    def __init__(self, db_path="logs.db", path="schema.sql"):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA synchronous=NORMAL;")
        self.conn.row_factory = sqlite3.Row
        self._init_schema(path)

    def _init_schema(self, path: str):
        # Run schema.sql only if DB is new or missing tables
        tables = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='logs';"
        ).fetchone()
        if not tables:
            with open(path, "r") as f:
                self.conn.executescript(f.read())
            self.conn.commit()

    def bulk_insert(self, logs: list[dict]):
        """Insert multiple log entries at once for efficiency."""
        if not logs:
            print("Nothing to insert.")
            return


        defaults = {
            "timestamp": None,
            "service": None,
            "level": None,
            "source_file": None,
            "message": None,
            "client_ip": None,
            "user": None,
            "status_code": None,
            "metadata": "{}"
        }

        prepared = []
        for log in logs:
            # merge defaults with each log entry
            entry = {**defaults, **log}
            entry["metadata"] = json.dumps(entry.get("metadata", {}))
            prepared.append(entry)

        with self._lock:
            self.conn.executemany("""
                INSERT INTO logs (timestamp, service, level, source_file, message, client_ip, user, status_code, metadata)
                VALUES (:timestamp, :service, :level, :source_file, :message, :client_ip, :user, :status_code, :metadata)
                """, prepared)

            self.conn.commit()

    def query(self, service=None, limit=10):
        """Retrieve recent logs, optionally filtered by service."""
        with self._lock:
            if service:
                rows = self.conn.execute(
                    "SELECT * FROM logs WHERE service=? ORDER BY timestamp DESC LIMIT ?",
                    (service, limit)
                ).fetchall()
            else:
                rows = self.conn.execute(
                    "SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?",
                    (limit,)
                ).fetchall()
            return [dict(row) for row in rows]

    def close(self):
        self.conn.close()
