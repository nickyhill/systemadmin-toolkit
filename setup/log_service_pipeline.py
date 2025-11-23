#!/usr/bin/env python3
import time
import logging
from app.log_pipeline import LogPipeline
from storage.storage import Storage

INTERVAL = 120 # seconds between cycles

def main():
    # Set up logging for backend
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("This message will go to stdout and be captured by journalctl.")
    logger.warning("A warning message captured by journalctl.")

    storage = Storage("logs.db", "storage/schema.sql", logger)
    pipeline = LogPipeline(storage)
    interval = INTERVAL

    while True:
        try:
            pipeline.run_pipeline_once(logger)
            print("Logs collected.")
        except Exception as e:
            print(f"Error collecting logs: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    main()
