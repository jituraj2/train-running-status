import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live-status')
def live_status():
    train_number = request.args.get('train_number')
    departure_date = request.args.get('departure_date')

    if not train_number or not departure_date:
        return jsonify({"error": "Missing train_number or departure_date"}), 400

    url = "https://indian-railway-irctc.p.rapidapi.com/api/trains/v1/train/status"
    querystring = {
        "departure_date": departure_date,
        "isH5": "true",
        "client": "web",
        "train_number": train_number
    }
    headers = {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
        "x-rapidapi-host": os.getenv("RAPIDAPI_HOST"),
        "x-rapid-api": "rapid-api-database"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": "Failed to fetch train status", "details": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
