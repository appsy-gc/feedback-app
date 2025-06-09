from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",  
    "http://localhost:8080",  
    "feedback-app-alb-128255988.ap-southeast-2.elb.amazonaws.com"  
])
DATABASE = "db.sqlite3"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            comment TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/submit", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    name = data.get("name")
    comment = data.get("comment")
    
    if not name or not comment:
        return jsonify({"error": "Missing name or comment"}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (name, comment) VALUES (?, ?)", (name, comment))
    conn.commit()
    conn.close()

    return jsonify({"message": "Feedback submitted successfully"}), 201

@app.route("/healthz", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    print("Initialising DB...")
    init_db()
    print("Starting Flask server...")
    app.run(debug=False, host="0.0.0.0")
