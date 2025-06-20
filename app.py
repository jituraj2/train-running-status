from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # Set this in Render env
RAPIDAPI_HOST = "indian-railway-irctc.p.rapidapi.com"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/live-status")
def live_status():
    train_number = request.args.get("train_number")
    departure_date = request.args.get("departure_date")
    isH5 = request.args.get("isH5", "true")  # default true
    client = request.args.get("client", "web")  # default web

    if not train_number or not departure_date:
        return jsonify({"error": "Missing train number or departure date"}), 400

    url = "https://indianrailapi.com/api/v2/livetrainstatus/apikey/{}/trainnumber/{}/date/{}/".format(
        API_KEY, train_number, departure_date
    )

    # If you're using another API endpoint with query params, use:
    # params = {
    #     "train_number": train_number,
    #     "departure_date": departure_date,
    #     "isH5": isH5,
    #     "client": client
    # }

    try:
        response = requests.get(url)  # or use `params=params` if using a query-string based API
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": "Failed to fetch live status", "details": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
