import os, json, requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RAPIDAPI_KEY = os.environ.get("e8b4f34e88msh27c8b188080aee4p1d9dc6jsn6bdc0e3dbae4")
RAPIDAPI_HOST = "train-running-status-indian-railways.p.rapidapi.com"

def call_rapidapi(endpoint, params=None, payload=None):
    url = f"https://{RAPIDAPI_HOST}/{endpoint}"
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY,
        "Content-Type": "application/json"
    }
    if params:
        resp = requests.get(url, headers=headers, params=params)
    else:
        resp = requests.post(url, headers=headers, json=payload)
    return resp.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/live-status', methods=['POST'])
def live_status():
    train_no = request.get_json().get("trainNo")
    if not train_no:
        return jsonify({"error": "Provide 'trainNo'"}), 400

    result = call_rapidapi("getRunningTrain", params={"train": train_no})
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
