from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Allow browser to talk to Flask

# Creative greetings for the chatbot
greetings = [
    "Hello! Welcome, I will be your guide for this amazing trip!",
    "Hi there! I’m your friendly travel companion, ready to assist you!",
    "Hey! Let’s explore together. I’ll keep you safe and guide you!",
    "Welcome! I’ll be your companion and guide during your journey!",
    "Hello! Ready for adventure? I’m here to help you every step of the way!"
]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    language = data.get("language", "en-US")  # Selected language
    gender = data.get("gender", "female")    # Selected voice

    # If user says hello, greet creatively
    if any(word in user_message.lower() for word in ["hi","hello","hey","hii","hola"]):
        reply_message = random.choice(greetings)
    else:
        # Default reply (can expand later with real place info)
        reply_message = f"You said: {user_message}. I’ll help you explore safely!"

    return jsonify({
        "reply": reply_message,
        "language": language,
        "gender": gender
    })

if __name__ == "__main__":
    app.run(debug=True)
