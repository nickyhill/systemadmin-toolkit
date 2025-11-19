from flask import jsonify, request, render_template
from app import app, storage
from app.log_pipeline import LogPipeline

pipeline = LogPipeline(storage)

@app.route('/')
@app.route('/index')
def index():
    logs = storage.query(limit=100)
    stats = storage.conn.execute("""
            SELECT service, COUNT(*) AS count
            FROM logs
            GROUP BY service
            ORDER BY count DESC
        """).fetchall()

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

@app.route("/api/collect", methods=["POST"])
def collect_logs():
    pipeline.run_pipeline_once()
    return jsonify({"status": "Logs collected"})
