import os
import http.client
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RAPIDAPI_HOST = "trains.p.rapidapi.com"
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
print("RAPIDAPI_KEY:", RAPIDAPI_KEY)


def make_rapidapi_post(path, payload):
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST,
        'Content-Type': "application/json"
    }
    conn.request("POST", path, json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search-trains', methods=['GET'])
def search_trains():
    search_query = request.args.get('search')
    if not search_query:
        return jsonify({"error": "Please provide search query parameter"}), 400

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

        # Optional check for proper response
        if not isinstance(result, dict) or 'message' not in result:
            return jsonify({"error": "Unexpected API response", "raw": result}), 500

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Failed to fetch live status", "details": str(e)}), 500



@app.route('/train-route', methods=['POST'])
def train_route():
    data = request.get_json()
    train_no = data.get('trainNo')

    if not train_no:
        return jsonify({"error": "Please provide 'trainNo' in JSON body"}), 400

    payload = {
        "trainNo": train_no
    }

    try:
        result = make_rapidapi_post("/v1/railways/train/route", payload)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Failed to fetch train route", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
