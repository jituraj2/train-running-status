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

@app.route('/live-status', methods=['GET'])
def live_status():
    train_no = request.args.get("trainNo")
    start_day = request.args.get("startDay", "1")

    if not train_no:
        return jsonify({"error": "Please provide 'trainNo'"}), 400

    url = f"https://{RAPIDAPI_HOST}/api/v1/liveTrainStatus"
    headers = {
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY
    }
    params = {
        "trainNo": train_no,
        "startDay": start_day
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": "API request failed", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
