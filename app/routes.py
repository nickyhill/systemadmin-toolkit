import logging
from flask import jsonify, request, render_template
from app import app
from storage.storage import Storage
from anomaly.anomaly_pipline import run_anomaly_pipeline

# initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info("This message will go to stdout and be captured by journalctl.")
logger.warning("A warning message captured by journalctl.")

# initialized storage for db query by api
storage = Storage("logs.db", "storage/schema.sql", logger=logger)

@app.route('/')
@app.route('/dashboard', methods=['GET', 'POST'])
def index():
    anomalies = None
    if request.method == "POST":
        # Run pipeline on button click
        anomalies_df = run_anomaly_pipeline()
        anomalies = anomalies_df[anomalies_df["anomaly"] == True].to_dict(orient="records")
    return render_template("dashboard.html", anomalies=anomalies)


@app.route('/logs')
def dis_logs():
    logs = storage.query()
    stats = storage.conn.execute("""
            SELECT service, source_file, COUNT(*) AS count
            FROM logs
            GROUP BY service, source_file
            ORDER BY service, count DESC
        """).fetchall()
    print(stats)
    return render_template('index.html', logs=logs, stats=stats)

@app.route("/api/logs", methods=["GET"])
def get_logs():
    service = str(request.args.get("service", default="system"))
    limit = int(request.args.get("limit", default=20))
    print("Routes DEBUG: ", service, limit)
    logs = storage.query(service=service, limit=limit)
    print("Length of the logs: ", len(logs))
    return jsonify(logs)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    stats = storage.conn.execute("""
        SELECT service, COUNT(*) AS count
        FROM logs
        GROUP BY service
        ORDER BY count DESC
    """).fetchall()
    return jsonify([dict(row) for row in stats])

