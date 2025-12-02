import logging
import json
from collector.collector import Collector

if __name__ == '__main__':
    # initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    collector = Collector(logger=logger)
    logs = collector.collect()
    print(f"Collected {len(logs)}")
    print(json.dumps(logs[:10], indent=4))
