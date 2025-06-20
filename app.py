from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/live-status')
def live_status():
    train_number = request.args.get('train_number')
    departure_date = request.args.get('departure_date')

    if not train_number or not departure_date:
        return jsonify({'error': 'Missing train_number or departure_date'}), 400

    url = "https://indian-railway-irctc.p.rapidapi.com/api/trains/v1/train/status"
    headers = {
        "x-rapidapi-host": "indian-railway-irctc.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {
        "train_number": train_number,
        "departure_date": departure_date,
        "isH5": "true",
        "client": "web"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # raises HTTPError for 4xx/5xx
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        print("🔴 Request failed:", e)
        return jsonify({'error': 'Failed to fetch live status', 'details': str(e)}), 500
