import logging
from collector.collector import Collector

if __name__ == '__main__':
    # initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("This message will go to stdout and be captured by journalctl.")
    logger.warning("A warning message captured by journalctl.")

    collector = Collector(logger=logger)
    logs = collector.collect()
    print(f"Collected {len(logs)}", logs[0:4])
