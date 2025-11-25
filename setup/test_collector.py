from collector.collector import Collector
import logging




if __name__ == '__main__':
    # initialize logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.info("This message will go to stdout and be captured by journalctl.")
    logger.warning("A warning message captured by journalctl.")

    collector = Collector(logger=logger)
    logs = collector.collect()
    print(f"Collected {len(logs)}", logs[0:4])
