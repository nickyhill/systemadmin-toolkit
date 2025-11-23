import os
import re
from datetime import datetime

## Collector Class that collects and parses logs

class Collector:
    def __init__(self, logger=None, apache_dir="/var/log/apache2/", system_dir="/var/log/"):
        self.apache_dir = apache_dir
        self.system_dir = system_dir
        self.system_logs = ["syslog", "auth.log", "cron.log"]
        self.logger = logger
        self.LOG_TS_REGEX = re.compile(r'^([A-Z][a-z]{2}\s+\d{1,2}\s+\d\d:\d\d:\d\d)')

    # Grabs logs definned in the constructor,
    # then formats and returns a list of dicts
    def collect(self) -> list[dict]:
        logs = []
        self.logger.info("Collecting logs...")
        for name in self.system_logs:
            path = os.path.join(self.system_dir, name)
            if not os.path.exists(path):
                continue
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    entry = {
                        "timestamp": self.parse_timestamp(line),
                         "message" : line.strip(),
                        "service": "system",
                        "source_file": name,
                        "raw": line
                    }
                    print(line.strip())
                    logs.append(entry)
        return logs



    def parse_timestamp(self, line: str):
        match = self.LOG_TS_REGEX.match(line)
        if not match:
            return None

        ts_str = match.group(1)
        # syslog timestamps have no year; add current year
        current_year = datetime.now().year
        ts_with_year = f"{ts_str} {current_year}"

        return datetime.strptime(ts_with_year, "%b %d %H:%M:%S %Y")