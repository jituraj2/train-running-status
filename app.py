from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__, template_folder='templates')

# Ensure your RapidAPI key is set as an environment variable
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')  # Paste key for local testing if needed

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
        "X-RapidAPI-Key": RAPIDAPI_KEY or "PASTE_YOUR_KEY_HERE",
        "X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"
    }
    params = {
        "train_number": train_number,
        "departure_date": departure_date,
        "isH5": "true",
        "client": "web"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as errh:
        return jsonify({'error': 'HTTP error', 'details': str(errh)}), 502
    except Exception as e:
        return jsonify({'error': 'Failed to fetch train status', 'details': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
