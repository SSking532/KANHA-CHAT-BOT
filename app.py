from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Dummy endpoint for chatbot testing
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    language = data.get("language", "en")
    gender = data.get("gender", "female")

    # For now, just return a mock response
    response = {
        "reply": f"Hello! You said: {user_message}",
        "language": language,
        "voice_gender": gender
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
