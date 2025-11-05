
from collector.collector import Collector
from parser.parser import Parser
if __name__ == '__main__':
    collector = Collector()
    collected = collector.collect()
    print(f"Collected {len(collected)} log entries")

    parser = Parser(collected)

