

CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            service TEXT NOT NULL,
            level TEXT,
            source_file TEXT,..
            message TEXT,
            client_ip TEXT,
            user TEXT,
            status_code INTEGER,
            metadata JSON
);

CREATE INDEX IF NOT EXISTS idx_logs_service_time ON logs(service, timestamp);