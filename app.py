import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/live-status')
def live_status():
    train_number = request.args.get('train_number')
    departure_date = request.args.get('departure_date')

    if not train_number or not departure_date:
        return jsonify({"error": "Missing parameters"}), 400

    api_key = os.getenv("RAIL_API_KEY")
    if not api_key:
        return jsonify({"error": "API key not set"}), 500

    url = f"https://indianrailapi.com/api/v2/livetrainstatus/apikey/{api_key}/trainnumber/{train_number}/date/{departure_date}/"

    try:
        response = requests.get(url)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # ✅ Render requires this
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
