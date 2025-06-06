from flask import Flask
import os

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

@app.route("/")
def home():
    return "Train running status backend is live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
