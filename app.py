from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

RAPID_API_KEY = os.getenv("RAPID_API_KEY")  # Set this in your environment on Render or locally

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/live-status')
def live_status():
    train_number = request.args.get("train_number")
    departure_date = request.args.get("departure_date")

    if not train_number or not departure_date:
        return jsonify({'error': 'Missing train_number or departure_date'}), 400

    url = "https://indian-railway-irctc.p.rapidapi.com/api/trains/v1/train/status"
    querystring = {
        "train_number": train_number,
        "departure_date": departure_date,
        "isH5": "true",
        "client": "web"
    }

    headers = {
        "x-rapidapi-host": "indian-railway-irctc.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapid-api": "rapid-api-database"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check if valid station list is returned
        if data.get("body") and isinstance(data["body"].get("stations"), list):
            return jsonify(data)
        else:
            return jsonify({"error": "Invalid API response or missing data"}), 502
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "API request failed", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
