import os
import time

import mysql.connector
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        connection_timeout=5,
    )

@app.route("/")
def home():
    return """
    <h1>Flask + MySQL 2-Tier Application</h1>
    <p>Deployed on AWS EC2 using Docker Compose.</p>
    <p><a href="/health">Check application health</a></p>
    <p><a href="/db-health">Check database connection</a></p>
    """

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

@app.route("/db-health")
def db_health():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(database="connected", result=result[0]), 200
    except mysql.connector.Error:
        app.logger.exception("Database health check failed")
        return jsonify(database="unavailable"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
