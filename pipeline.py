from collector.collector import Collector
from parser.parser import Parser
from storage.storage import Storage

collector = Collector()
parser = Parser(collector)

POLL_INTERVAL = 5  # seconds between collections

def run_pipeline_once():
    """Collect logs, parse, and store."""
    parsed = parser.parse()
    if not parsed:
        return
    else:
        storage.bulk_insert(parsed)
        print("Inserted %d logs", len(parsed))