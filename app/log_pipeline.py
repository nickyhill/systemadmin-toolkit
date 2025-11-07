from collector.collector import Collector
from storage.storage import Storage

class LogPipeline:

    def __init__(self, storage):
        self.collector = Collector()
        self.storage = storage
        self.POLL_INTERVAL = 5  # seconds between collections

    def run_pipeline_once(self) -> None:
        """Collect logs, parse, and store."""
        raw_logs = self.collector.collect()  # collect new logs each time
        if not raw_logs:
            return
        else:
            self.storage.bulk_insert(raw_logs)
            print(f"Inserted {len(raw_logs)} logs")