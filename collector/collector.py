import os
from datetime import datetime

## Collector Class that collects and parses logs

class Collector:
    def __init__(self, apache_dir="/var/log/apache2/", system_dir="/var/log/"):
        self.apache_dir = apache_dir
        self.system_dir = system_dir
        self.system_logs = ["syslog", "auth.log", "cron.log"]

    # Grabs logs definned in the constructor,
    # then formats and returns a list of dicts
    def collect(self) -> list[dict]:
        logs = []
        for name in self.system_logs:
            path = os.path.join(self.system_dir, name)
            if not os.path.exists(path):
                continue
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    entry = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "service": "system",
                        "source_file": name,
                        "raw": line.strip()
                    }
                    print(line.strip())
                    logs.append(entry)
        return logs