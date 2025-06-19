@app.route('/live-status')
def live_status():
    train_no = request.args.get("train_number")
    departure_date = request.args.get("departure_date")
    isH5 = request.args.get("isH5", "true")
    client = request.args.get("client", "web")

    if not train_no or not departure_date:
        return jsonify({"error": "Train number and departure date are required"}), 400

    payload = {
        "trainNo": train_no,
        "departure_date": departure_date,
        "isH5": isH5,
        "client": client
    }

    try:
        result = make_rapidapi_post("/trainLiveStatus", payload)
        print("🔍 API raw response:", json.dumps(result, indent=2))

        body = result.get("data", {}).get("body")
        if not body:
            return jsonify({
                "error": "Invalid API structure",
                "note": "Missing 'body' in result",
                "raw_response": result
            }), 500

        return jsonify({
            "train_status_message": body.get("train_status_message", "Not available"),
            "current_station": body.get("current_station", "Unknown"),
            "terminated": body.get("terminated", False),
            "time_of_availability": body.get("time_of_availability", "Unknown"),
            "stations": body.get("stations", []),
            "title": result.get("data", {}).get("title", "Live Status"),
            "body": body
        })

    except Exception as e:
        return jsonify({
            "error": "Exception occurred while fetching status",
            "details": str(e)
        }), 500
