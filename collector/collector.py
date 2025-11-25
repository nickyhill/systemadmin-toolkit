import os
import re
from datetime import datetime

class Collector:
    def __init__(self, logger=None, apache_dir="/var/log/apache2/", system_dir="/var/log/"):
        self.apache_dir = apache_dir
        self.system_dir = system_dir
        self.system_logs = ["syslog", "auth.log"]
        self.apache_logs = ["access.log", "error.log"]
        self.logger = logger

        ## Syslog and auth.log regex format
        # Matches: timestamp, hostname, service, message
        self.LOG_REGEX = re.compile(
            r"""^
            (?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))\s+
            (?P<host>\S+)\s+
            (?P<service>\w+):\s+
            (?P<msg>.*)
            """,
            re.VERBOSE,
        )

    def collect(self) -> list[dict]:
        logs = []
        if self.logger:
            self.logger.info("Collecting logs...")

        for name in self.system_logs:
            path = os.path.join(self.system_dir, name)
            if not os.path.exists(path):
                continue

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    parsed = self.parse_line(line, name)
                    if parsed:
                        logs.append(parsed)
                    else:
                        continue

        return logs

    def parse_line(self, line: str, file: str):
        m = self.LOG_REGEX.match(line)
        if not m:
            return None

        ts_str = m.group("ts")
        try:
            timestamp = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except ValueError:
            timestamp = None

        return {
            "timestamp": timestamp.isoformat() if timestamp else None,
            "service": m.group("service"),
            "message": m.group("msg").strip(),
            "source_file": file,
            "raw": line.strip(),
        }
