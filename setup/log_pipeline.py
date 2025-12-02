from collector.collector import Collector
from storage.storage import Storage

class LogPipeline:

    def __init__(self, storage):
        self.storage = storage
        self.POLL_INTERVAL = 0 # seconds between collections
        self.logger = storage.logger
        self.collector = Collector(logger=self.logger)

    def run_pipeline_once(self) -> None:
        self.logger.info("Collecting logs...")
        raw_logs = self.collector.collect()  # collect new logs each time
        if not raw_logs:
            return
        else:
            self.storage.bulk_insert(raw_logs)
            print(f"Inserted {len(raw_logs)} logs")