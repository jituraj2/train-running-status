from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Train Running Status Backend is live!"

@app.route('/status')
def status():
    train = request.args.get('train')
    date = request.args.get('date')

    if not train or not date:
        return jsonify({"error": "Please provide train and date parameters"}), 400

    # Example response, replace this with your actual logic
    response = {
        "train": train,
        "date": date,
        "status": "Running on time",
        "last_station": "Station XYZ",
        "next_station": "Station ABC",
        "expected_arrival": "14:30"
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
