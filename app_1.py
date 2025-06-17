import os, requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set your RapidAPI key here or as an environment variable
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "your_rapidapi_key_here")
RAPIDAPI_HOST = "irctc1.p.rapidapi.com"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/live-status', methods=['POST'])
def live_status():
    data = request.get_json()
    train_no = data.get('trainNo')
    start_day = data.get('startDay')

    if not train_no or not start_day:
        return jsonify({"error": "trainNo and startDay are required"}), 400

    payload = {
        "trainNo": train_no,
        "startDay": start_day
    }

    try:
        result = make_rapidapi_post("/train/live/status", payload)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Failed to fetch live status", "details": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
