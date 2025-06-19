from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔁 Replace with your actual RapidAPI credentials
RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY"
RAPIDAPI_HOST = "indian-railway-irctc.p.rapidapi.com"

def make_rapidapi_post(endpoint, payload):
    url = f"https://{RAPIDAPI_HOST}{endpoint}"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.route("/live-status")
def live_status():
    train_no = request.args.get("train_number")
    departure_date = request.args.get("departure_date")
    isH5 = request.args.get("isH5", "true")
    client = request.args.get("client", "web")

    if not train_no or not departure_date:
        return jsonify({"error": "Train number and departure date are required"}), 400

    try:
        payload = {
            "trainNo": train_no,
            "departure_date": departure_date,
            "isH5": isH5,
            "client": client
        }

        result = make_rapidapi_post("/trainLiveStatus", payload)

        if result.get("status") != "success" or not result.get("body"):
            return jsonify({
                "error": "Invalid API structure or missing data",
                "raw": result
            }), 500

        return jsonify({
            "title": result.get("title", "Live Status"),
            "message": result.get("message"),
            "body": result["body"]
        })

    except Exception as e:
        return jsonify({"error": "Exception occurred", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
