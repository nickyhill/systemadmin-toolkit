
from collector.collector import Collector
from parser.parser import Parser
from storage.storage import Storage
from flask import Flask, jsonify, request

app = Flask(__name__)
storage = Storage("logs.db")


@app.route("/api/logs", methods=["GET"])
def get_logs():
    service = request.args.get("service")
    limit = int(request.args.get("limit", 20))
    logs = storage.query(service=service, limit=limit)
    return jsonify(logs)

@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = storage.conn
    stats = conn.execute("""
        SELECT service, COUNT(*) AS count
        FROM logs
        GROUP BY service
        ORDER BY count DESC
    """).fetchall()
    return jsonify([dict(row) for row in stats])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

