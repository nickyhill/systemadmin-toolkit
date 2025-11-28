import pandas as pd
import re
import numpy as np
from sklearn.preprocessing import StandardScaler
from anomaly.logai.preprocess.preprocessor import Preprocessor, PreprocessorConfig
from anomaly.logai.information_extraction.log_vectorizer import LogVectorizer, VectorizerConfig
from anomaly.logai.information_extraction.categorical_encoder import CategoricalEncoder, CategoricalEncoderConfig
from anomaly.logai.information_extraction.feature_extractor import FeatureExtractor, FeatureExtractorConfig
from anomaly.logai.analysis.anomaly_detector import AnomalyDetector, AnomalyDetectionConfig
from anomaly.logai.algorithms.anomaly_detection_algo.isolation_forest import IsolationForestDetector, IsolationForestParams

def run_anomaly_pipeline():
    # 1 Load log data
    #log_file = "/var/log/apache2/error.log"
    log_file = "error.log" # DEBUG DIR
    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    df = pd.DataFrame(lines, columns=["Content"])
    print("Total lines loaded:", len(df))

    # 2 Preprocess logs
    preprocessor = Preprocessor(PreprocessorConfig(custom_delimiters_regex=[]))
    df["Content"], _ = preprocessor.clean_log(df["Content"])


    def extract_fields(logline):
        """
        Extract timestamp, module, level, pid, tid, and message
        from an Ubuntu Apache error.log line.
        """
        pattern = (
            r"^\[(?P<timestamp>[^\]]+)\] "  # timestamp
            r"\[(?P<module>[^:]+):(?P<level>[^\]]+)\] "  # module:level
            r"\[pid (?P<pid>\d+):tid (?P<tid>\d+)\] "  # pid:tid
            r"(?P<message>.*)$"  # message
        )

        m = re.match(pattern, logline)
        if m:
            return pd.Series({
                "timestamp": m.group("timestamp"),
                "module": m.group("module"),
                "level": m.group("level"),
                "pid": int(m.group("pid")),
                "tid": int(m.group("tid")),
                "message": m.group("message")
            })
        else:
            # fallback if it doesn't match
            return pd.Series({
                "timestamp": None,
                "module": None,
                "level": None,
                "pid": None,
                "tid": None,
                "message": logline
            })

    parsed_loglines = df["Content"].apply(extract_fields)
    print("First 5 parsed loglines:")
    print(parsed_loglines.head())

    # 4 Vectorize log messages (TF-IDF)
    vectorizer = LogVectorizer(VectorizerConfig(algo_name="tfidf"))
    messages = parsed_loglines["message"].astype(str)
    vectorizer.fit(messages)
    log_vectors = vectorizer.transform(messages)
    print("Vector shape:", log_vectors.shape)

    # 5 Encode categorical attributes
    encoder = CategoricalEncoder(CategoricalEncoderConfig(name="label_encoder"))
    attributes_encoded = encoder.fit_transform(parsed_loglines[["level"]])

    # 6 Convert timestamp to datetime
    timestamps = pd.to_datetime(parsed_loglines["timestamp"], format="%a %b %d %H:%M:%S %Y", errors="coerce")

    # 7 Feature extraction
    feature_extractor = FeatureExtractor(FeatureExtractorConfig(max_feature_len=100))
    _, feature_vector = feature_extractor.convert_to_feature_vector(
        log_vectors, attributes_encoded, timestamps
    )

    # Convert feature_vector to numeric only (exclude datetime columns)
    # If feature_vector is a DataFrame, drop non-numeric columns
    # Keep numeric columns but as DataFrame
    if isinstance(feature_vector, pd.DataFrame):
        feature_vector_numeric = feature_vector.select_dtypes(include=[np.number])
    else:
        feature_vector_numeric = pd.DataFrame(feature_vector,
                                              columns=[f"f{i}" for i in range(feature_vector.shape[1])])

    print("Feature vector shape:", feature_vector_numeric.shape)

    # 8 Train anomaly detector using Isolation Forest
    scaler = StandardScaler()
    feature_vector_scaled = pd.DataFrame(
         scaler.fit_transform(feature_vector_numeric),
         columns=feature_vector_numeric.columns,
         index=feature_vector_numeric.index
     )
    iso_params = IsolationForestParams(
        n_estimators=100,
        contamination=0.01,  # roughly 1% anomalies expected
        random_state=42,
        warm_start=False
    )
    anomaly_detector = AnomalyDetector(
        AnomalyDetectionConfig(algo_name="isolation_forest", algo_params=iso_params)
    )
    anomaly_detector.fit(feature_vector_scaled)

    # 9 Predict anomalies
    anomalies = anomaly_detector.predict(feature_vector_scaled)
    anomalies_bool = anomalies["anom_score"] == -1  # sklearn IsolationForest marks anomalies as -1

    # Attach anomaly column to parsed logs
    result_df = parsed_loglines.copy()
    result_df["anomaly"] = anomalies_bool

    print("Number of anomalies detected:", anomalies_bool.sum())
    return result_df


    # # 8 Train anomaly detector
    # scaler = StandardScaler()
    # feature_vector_scaled = pd.DataFrame(
    #     scaler.fit_transform(feature_vector_numeric),
    #     columns=feature_vector_numeric.columns,
    #     index=feature_vector_numeric.index
    # )
    #
    # algo_params = OneClassSVMParams(nu=0.5, kernel="rbf")
    # anomaly_detector = AnomalyDetector(
    #     AnomalyDetectionConfig(algo_name="one_class_svm", algo_params=algo_params)
    # )
    # anomaly_detector.fit(feature_vector_scaled)
    #
    # # 9 Predict anomalies
    # anomalies = anomaly_detector.predict(feature_vector_scaled)
    # # Ensure anomalies are boolean
    # anomalies_bool = anomalies["anom_score"].astype(bool)
    # # Add anomaly column to your parsed logs
    # result_df = parsed_loglines.copy()
    # result_df["anomaly"] = anomalies_bool
    #
    # print("Number of anomalies detected:", anomalies_bool.sum())
    #
    # # ✅ Return the DataFrame so your dashboard can display it
    # return result_df