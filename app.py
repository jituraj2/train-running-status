import os

port = int(os.environ.get("PORT", 5000))  # fallback to 5000 locally
app.run(host="0.0.0.0", port=port)
