import logging
import json
from anomaly.anomaly_pipline import run_anomaly_pipeline

if __name__ == '__main__':
    # initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("Starting anomaly test")
    anomalies_df = run_anomaly_pipeline()
    anomalies_df_pos = anomalies_df[anomalies_df['anomaly'] == True]
    logger.info(f"Results:\n  {anomalies_df_pos}")
