from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # Set this in Render environment
RAPIDAPI_HOST = "indian-railway-irctc.p.rapidapi.com"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/live-status')
def live_status():
    train_number = request.args.get('train_number')
    departure_date = request.args.get('departure_date')

    if not train_number or not departure_date:
        return jsonify({'error': 'Missing train_number or departure_date'}), 400

    url = "https://indian-railway-irctc.p.rapidapi.com/apiendpoint"

    querystring = {
        "train_number": train_number,
        "departure_date": departure_date,
        "isH5": "true",
        "client": "web"
    }

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': 'Failed to fetch live status', 'details': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
