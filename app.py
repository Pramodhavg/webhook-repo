from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB connection string
MONGO_URI = "mongodb+srv://pramodhavg:Ilikemymummy12@cluster0.q36lt32.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client['webhook_db']
collection = db['events']

@app.route('/')
def home():
    return "Webhook Receiver is Running!"

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json

    # Detect event type from GitHub header
    action_type = request.headers.get('X-GitHub-Event', 'unknown').upper()
    print(f"Received event: {action_type}")

    if action_type == "PUSH":
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1]
        timestamp = data['head_commit']['timestamp']
        request_id = data['head_commit']['id']

        record = {
            "request_id": request_id,
            "author": author,
            "action": "PUSH",
            "from_branch": None,
            "to_branch": to_branch,
            "timestamp": timestamp
        }

        collection.insert_one(record)
        return jsonify({"message": "Push event saved"}), 200

    return jsonify({"message": "Unhandled event type"}), 200

@app.route('/test-insert')
def test_insert():
    test_data = {
        "request_id": "123456",
        "author": "test_user",
        "action": "PUSH",
        "from_branch": None,
        "to_branch": "main",
        "timestamp": "2025-07-10T10:00:00Z"
    }
    collection.insert_one(test_data)
    return "Test data inserted!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
