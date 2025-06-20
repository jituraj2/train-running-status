from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Set your RapidAPI Key in environment or paste directly here for local testing
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # e.g., "your_actual_key"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/live-status")
def live_status():
    train_number = request.args.get("train_number")
    departure_date = request.args.get("departure_date")

    if not train_number or not departure_date:
        return jsonify({"error": "Missing parameters"}), 400

    url = "https://indian-railway-irctc.p.rapidapi.com/api/trains/v1/train/status"
    headers = {
        "x-rapidapi-host": "indian-railway-irctc.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapid-api": "rapid-api-database"
    }
    params = {
        "train_number": train_number,
        "departure_date": departure_date,
        "isH5": "true",
        "client": "web"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch train status", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
