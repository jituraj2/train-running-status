import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ Use your actual RapidAPI key or set it via environment variable
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "your_real_key_here")
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
    return render_template('index.html')  # Make sure templates/index.html exists

@app.route('/live-status', methods=['POST'])
def live_status():
    data = request.get_json()
    train_no = data.get('trainNo')
    start_day = data.get('startDay', "1")  # Default to 1 (today) if not provided

    if not train_no:
        return jsonify({"error": "trainNo is required"}), 400

    payload = {
        "trainNo": str(train_no),
        "startDay": str(start_day)
    }

    try:
        result = make_rapidapi_post("/trainLiveStatus", payload)

        if result.get("status") is False or result.get("data", {}).get("success") is False:
            return jsonify({
                "error": result.get("data", {}).get("message", "Unknown error"),
                "details": result
            }), 400

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Failed to fetch live status", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
