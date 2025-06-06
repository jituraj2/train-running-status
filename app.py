import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Train Running Status Backend is live!"

@app.route('/status')
def status():
    train = request.args.get('train')
    date = request.args.get('date')  # Optional depending on API

    if not train:
        return jsonify({"error": "Please provide train number"}), 400

    url = f"https://indian-railway-irctc.p.rapidapi.com/trainStatus"
    querystring = {"trainNo": train}

    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        if not data.get("train"):
            return jsonify({"error": "No data found", "response": data}), 404

        return jsonify({
            "train_name": data["train"]["name"],
            "train_number": data["train"]["number"],
            "position": data.get("position"),
            "route": data.get("route")  # optional full route
        })

    except Exception as e:
        return jsonify({"error": "Failed to fetch train data", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
