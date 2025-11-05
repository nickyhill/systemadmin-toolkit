import sqlite3
import json
from pathlib import Path

class Storage:
    def __init__(self, db_path="logs.db"):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            service TEXT NOT NULL,
            level TEXT,
            source_file TEXT,
            message TEXT NOT NULL,
            client_ip TEXT,
            user TEXT,
            status_code INTEGER,
            metadata JSON
        );
        """)
        self.conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_logs_service_time
        ON logs(service, timestamp);
        """)
        self.conn.commit()

    def insert_log(self, log_entry: dict):
        """Insert one parsed log entry into the database."""


        self.conn.execute("""
        INSERT INTO logs (timestamp, service, level, source_file, message, client_ip, user, status_code, metadata)
        VALUES (:timestamp, :service, :level, :source_file, :message, :client_ip, :user, :status_code, :metadata)
        """, {
            "timestamp": log_entry.get("timestamp"),
            "service": log_entry.get("service"),
            "level": log_entry.get("level"),
            "source_file": log_entry.get("source_file"),
            "message": log_entry.get("message"),
            "client_ip": log_entry.get("client_ip"),
            "user": log_entry.get("user"),
            "status_code": log_entry.get("status_code"),
            "metadata": json.dumps(log_entry.get("metadata", {}))
        })
        self.conn.commit()

    def bulk_insert(self, logs: list[dict]):
        """Insert multiple log entries at once for efficiency."""
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

        entry = {**defaults, **logs}
        entry["metadata"] = json.dumps(entry.get("metadata", {}))

        self.conn.executemany("""
        INSERT INTO logs (timestamp, service, level, source_file, message, client_ip, user, status_code, metadata)
        VALUES (:timestamp, :service, :level, :source_file, :message, :client_ip, :user, :status_code, :metadata)
        """, [
            {
                **entry,
                "metadata": json.dumps(log.get("metadata", {}))
            } for log in entry
        ])
        self.conn.commit()

    def query(self, service=None, limit=10):
        """Retrieve recent logs, optionally filtered by service."""
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
