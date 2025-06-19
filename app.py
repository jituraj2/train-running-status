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

    url = "https://indianrailapi.com/api/v2/livetrainstatus/apikey/YOUR_API_KEY/trainnumber/{}/date/{}/".format(
        train_number, departure_date)

    # If you're using RapidAPI, use this instead:
    # url = "https://rahilkhan224-indian-railway-irctc-v1.p.rapidapi.com/liveTrainStatus"
    # params = {"departure_date": departure_date, "train_number": train_number, "isH5": "true", "client": "web"}
    # headers = {"X-RapidAPI-Key": "YOUR_KEY", "X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"}

    try:
        response = requests.get(url)  # or requests.get(url, headers=headers, params=params)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
