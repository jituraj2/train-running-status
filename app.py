import os
import json
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace this with your actual RapidAPI key or use environment variable
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "e8b4f34e88msh27c8b188080aee4p1d9dc6jsn6bdc0e3dbae4")
RAPIDAPI_HOST = "trains.p.rapidapi.com"

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
    return render_template('index.html')  # Should exist in /templates/index.html

@app.route('/search-trains', methods=['GET'])
def search_trains():
    search_query = request.args.get('search')
    if not search_query:
        return jsonify({"error": "Please provide search query"}), 400

    try:
        result = make_rapidapi_post("/v1/railways/trains/india", {"search": search_query})
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Failed to fetch train data", "details": str(e)}), 500

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
        result = make_rapidapi_post("/v1/railways/train/status", payload)

        if not isinstance(result, dict):
            return jsonify({"error": "Unexpected API response", "raw": result}), 500

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Failed to fetch live status", "details": str(e)}), 500

@app.route('/train-route', methods=['POST'])
def train_route():
    data = request.get_json()
    train_no = data.get('trainNo')

    if not train_no:
        return jsonify({"error": "Please provide 'trainNo'"}), 400

    try:
        result = make_rapidapi_post("/v1/railways/train/route", {"trainNo": train_no})
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Failed to fetch train route", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
