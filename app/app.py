from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

app = Flask(__name__)
todos = []

REQUESTS = Counter("todo_requests_total", "Total requests", ["endpoint"])

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/todos", methods=["GET"])
def list_todos():
    REQUESTS.labels(endpoint="list").inc()
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    REQUESTS.labels(endpoint="add").inc()
    item = {"id": len(todos) + 1, "title": request.json["title"]}
    todos.append(item)
    return jsonify(item), 201

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))