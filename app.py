@app.route('/status')
def status():
    import time

    train = request.args.get('train')
    date = request.args.get('date')  # format: YYYY-MM-DD

    if not train or not date:
        return jsonify({"error": "Please provide train and date parameters"}), 400

    api_key = os.environ.get('INDIANRAIL_API_KEY')

    # Convert date from YYYY-MM-DD to DD-MM-YYYY
    try:
        yyyy, mm, dd = date.split('-')
        formatted_date = f"{dd}-{mm}-{yyyy}"
    except:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Construct API URL
    url = f"https://indianrailapi.com/api/v2/livetrainstatus/apikey/{api_key}/trainnumber/{train}/date/{formatted_date}/"

    # Retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            data = response.json()

            if data.get("ResponseCode") == "200":
                current_station = data.get("CurrentStation", {})
                return jsonify({
                    "train": data.get("TrainNumber"),
                    "date": data.get("StartDate"),
                    "status": data.get("Message"),
                    "last_station": current_station.get("StationName"),
                    "next_station": (
                        data["TrainRoute"][int(current_station["SerialNo"]) + 1]["StationName"]
                        if current_station.get("SerialNo") and data.get("TrainRoute") else None
                    ),
                    "expected_arrival": current_station.get("ScheduleArrival")
                })
            elif attempt < max_retries - 1:
                time.sleep(2)
        except Exception as e:
            return jsonify({"error": "Error contacting IndianRailAPI", "details": str(e)}), 500

    # If all retries fail
    return jsonify({"error": "API Server busy after retries", "message": "Please try again later."}), 503
