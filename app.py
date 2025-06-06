import os
import requests
from flask import Flask, request, jsonify

# Load environment variables in local dev
if os.environ.get("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Train Running Status Backend is live!"

@app.route('/status')
def status():
    train = request.args.get('train')
    if not train:
        return jsonify({"error": "Train number required"}), 400

    url = "https://indian-railway-irctc.p.rapidapi.com/trainLiveStatus"
    querystring = {"trainNo": train}
    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Debug: log raw data
        print("RAW API RESPONSE:", data)

        if data.get("message") == "Invalid API Key":
            return jsonify({"error": "Invalid API Key", "raw": data}), 401

        if not data.get("train"):
            return jsonify({"error": "No train data found", "raw": data}), 404

        return jsonify({
            "train_name": data["train"]["name"],
            "train_number": data["train"]["number"],
            "position": data.get("position"),
            "route": data.get("route", [])
        })

    except Exception as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
