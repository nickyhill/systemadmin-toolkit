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

        ## access.log and error.log regex format
        # Matches: timestamp, hostname, service, message
        self.LOG_REGEX_APACHE = re.compile(
            r"""
            ^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})       # IPv4
            \s+.*?\[                               # skip dashes/ident fields until date
            (?P<ts>[^\]]+)                       # date/time inside brackets
            \]\s+
            (?P<op>GET|POST|PUT|DELETE|HEAD|PATCH|OPTIONS)\s+
            (?P<msg>.*)$                           # rest of the message
            """,
            re.VERBOSE,
        )

        self.LOG_REGEX_APACHE_ERROR = re.compile(
            r"""
            ^\[
            (?P<ts>[^]]+)
            \]\s+
            \[[^\]]*\]\s+
            \[[^\]]*\]\s+
            \[client\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\]\s+
            (?P<msg>.*)
            $""",
            re.VERBOSE,
        )



    def collect(self) -> list[dict]:
        logs = []
        if self.logger:
            self.logger.info("Collecting logs...")

        # Parse system logs
        for name in self.system_logs:
            path = os.path.join(self.system_dir, name)
            if not os.path.exists(path):
                self.logger.info(f"Log file does not exist: {path}")
                continue

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    parsed = self._parse_line(line, name)
                    if parsed:
                        logs.append(parsed)
                    else:
                        continue

        # Parse apache logs
        for name in self.apache_logs:
            path = os.path.join(self.apache_dir, name)
            if not os.path.exists(path):
                self.logger.info(f"Log file does not exist: {path}")
                continue

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    parsed = self._parse_line(line, name)
                    if parsed:
                        logs.append(parsed)
                    else:
                        continue

        return logs


    def _parse_line(self, line: str, file: str):
        if file in self.system_logs:
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

        elif file in self.apache_logs:
            m = self.LOG_REGEX_APACHE.match(line)
            if file == "error.log":
                m = self.LOG_REGEX_APACHE_ERROR.match(line)
            if not m:
                return None

            ts_str = m.group("ts")
            try:
                timestamp = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            except ValueError:
                timestamp = None

            return {
                "timestamp": timestamp.isoformat() if timestamp else None,
                "client_ip": m.group("ip"),
                "message": m.group("msg").strip(),
                "source_file": file,
                "status_code": m.group("op"),
                "raw": line.strip(),
            }
        self.logger.error("Failed to parse and return logs")
        return None