from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv('RAIL_API_KEY')  # Set this in your Render environment

@app.route('/live-status')
def live_status():
    train_number = request.args.get('train_number')
    departure_date = request.args.get('departure_date')

    if not train_number or not departure_date:
        return jsonify({'error': 'Missing train_number or departure_date'}), 400

    url = f"https://indianrailapi.com/api/v2/livetrainstatus/apikey/{API_KEY}/trainnumber/{train_number}/date/{departure_date}/"

    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch live status', 'details': str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)

