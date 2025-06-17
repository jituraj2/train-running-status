import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "your_real_rapidapi_key_here")
RAPIDAPI_HOST = "indian-railway-irctc.p.rapidapi.com"

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
    return render_template('index.html')

@app.route('/live-status', methods=['POST'])
def live_status():
    data = request.get_json()
    train_no = data.get('trainNo')

    if not train_no:
        return jsonify({"error": "Train number required"}), 400

    payload = { "trainNo": train_no }

    try:
        result = make_rapidapi_post("/trainLiveStatus", payload)
        print("🔎 API Response:", json.dumps(result, indent=2))  # Debugging

        # Safe extraction
        body = result.get("body")
        if not body or "stations" not in body:
            return jsonify({
                "error": "Invalid API response",
                "raw_response": result
            }), 500

        response = {
            "train_status_message": body.get("train_status_message", "N/A"),
            "current_station": body.get("current_station", "N/A"),
            "terminated": body.get("terminated", False),
            "stations": body.get("stations", [])
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch live status",
            "details": str(e)
        }), 500



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
