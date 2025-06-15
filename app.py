import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace with your actual RapidAPI Key or load from environment
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "your_real_key_here")
RAPIDAPI_HOST = "train-running-status-indian-railways.p.rapidapi.com"

def make_rapidapi_post(path, payload):
    url = f"https://{RAPIDAPI_HOST}{path}"
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

@app.route('/')
def home():
    return render_template('index.html')  # Must exist in templates/

@app.route('/live-status', methods=['POST'])
def live_status():
    data = request.get_json()
    train_no = data.get('trainNo')

    if not train_no:
        return jsonify({"error": "No train number provided"}), 400

    payload = {
        "trainNo": train_no
    }

    try:
        result = make_rapidapi_post("/trainLiveStatus", payload)

        if not isinstance(result, dict):
            return jsonify({"error": "Unexpected API response", "raw": result}), 500

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Failed to fetch live status", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
