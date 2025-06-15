import os, json, requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # Set in Render or your environment
RAPIDAPI_HOST = "train-running-status-indian-railways.p.rapidapi.com"

def rapidapi_post(endpoint, body):
    url = f"https://{RAPIDAPI_HOST}/{endpoint}"
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY,
        "Content-Type": "application/json"
    }
    resp = requests.post(url, headers=headers, json=body)
    return resp.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/live-status', methods=['POST'])
def live_status():
    train_no = request.get_json().get("trainNo")
    if not train_no:
        return jsonify({"error": "Provide 'trainNo'"}), 400

    try:
        data = rapidapi_post("liveTrainRunningStatus", {"trainNo": train_no})
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
