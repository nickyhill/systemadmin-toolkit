import random
import sys
import pandas as pd
from datetime import datetime, timedelta

# Modules and levels commonly seen in Ubuntu Apache error logs
modules = ["mpm_event", "core", "authz_core", "http2", "ssl"]
levels = ["notice", "warn", "error"]

# Normal messages (template-like)
normal_messages = [
    "AH00489: Apache/{version} (Ubuntu) configured -- resuming normal operations",
    "AH00094: Command line: '/usr/sbin/apache2'",
    "AH00558: apache2: Could not reliably determine the server's fully qualified domain name",
    "AH00163: Apache/2.4.58 (Ubuntu) configured -- resuming normal operations",
]

# Anomalous messages
anomalies = [
    "AH02545: Unexpected shutdown due to segmentation fault",
    "AH01234: Failed to start module {module} -- memory leak detected",
    "AH09999: Critical error: PID {pid} crashed",
]


def generate_log_line(timestamp, anomaly=False):
    module = random.choice(modules)
    level = random.choice(levels)
    pid = random.randint(1000, 5000)
    tid = random.randint(100000000000000, 200000000000000)

    if anomaly and random.random() < 0.7:  # ~70% chance to pick anomaly template
        msg_template = random.choice(anomalies)
        msg = msg_template.format(module=module, pid=pid)
    else:
        msg_template = random.choice(normal_messages)
        version = f"2.4.{random.randint(50, 60)}"
        msg = msg_template.format(version=version)

    ts_str = timestamp.strftime("%a %b %d %H:%M:%S.%f %Y")

    log_line = f"[{ts_str}] [{module}:{level}] [pid {pid}:tid {tid}] {msg}"
    return log_line


def generate_log_dataset(n_lines=3000, anomaly_ratio=0.05):
    start_time = datetime(2025, 6, 28)
    lines = []
    for i in range(n_lines):
        timestamp = start_time + timedelta(seconds=i * 2)  # 2 sec increments
        anomaly = random.random() < anomaly_ratio
        line = generate_log_line(timestamp, anomaly)
        lines.append(line)
    return pd.DataFrame(lines)


# Example usageS
df_logs = generate_log_dataset()
print(df_logs.head())
path = (sys.argv[1] + "/error.log")
with open(path, "a") as f:
    for idx in range(0, len(df_logs)):
        f.write(df_logs[0][idx] + '\n')


print(f"Generated {len(df_logs)} log lines and wrote to synthetic_apache_error.log")
