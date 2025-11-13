#!/usr/bin/env python3
import time
from app.log_pipeline import LogPipeline
from storage.storage import Storage

def main():
    storage = Storage("logs.db", "storage/schema.sql")
    pipeline = LogPipeline(storage)
    interval = 60  # seconds between cycles

    while True:
        try:
            pipeline.run_pipeline_once()
            print("Logs collected.")
        except Exception as e:
            print(f"Error collecting logs: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    main()
