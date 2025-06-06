import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

@app.route('/status')
def status():
    train = request.args.get('train')
    if not train:
        return jsonify({"error": "Train number required"}), 400

    url = "https://indian-railway-irctc.p.rapidapi.com/trainStatus"
    querystring = {"trainNo": train}
    headers = {
        "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "indian-railway-irctc.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    print("RAW API RESPONSE:", data)

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
