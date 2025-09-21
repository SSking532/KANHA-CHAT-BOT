from flask import Flask, request, jsonify
from flask_cors import CORS
import random, json, os
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)

# Load tourist places data
with open("places.json", "r", encoding="utf-8") as f:
    places_data = json.load(f)

# Creative greetings
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
    user_message = data.get("message", "").lower().strip()
    language = data.get("language", "en-US")
    gender = data.get("gender", "female")

    # 1. Greeting detection
    if any(word in user_message for word in ["hi", "hello", "hey", "hii", "hola"]):
        reply_message = random.choice(greetings)

    # 2. Check if user asked about a tourist place
    elif user_message in places_data:
        place = places_data[user_message]
        reply_message = (
            f"Here’s some info about {user_message.title()}:\n"
            f"History: {place['history']}\n"
            f"Famous Spots: {', '.join(place['famous_spots'])}\n"
            f"Emergency Numbers: {', '.join(place['emergency_numbers'])}\n"
            f"Past Accidents: {place['past_accidents']}"
        )

    else:
        reply_message = f"You said: {user_message}. I’ll help you explore safely!"

    # 3. Translate reply into selected language
    try:
        lang_code = language.split("-")[0]
        translated = GoogleTranslator(source="auto", target=lang_code).translate(reply_message)
        reply_message = translated
    except Exception as e:
        print("Translation failed:", e)

    return jsonify({
        "reply": reply_message,
        "language": language,
        "gender": gender
    })


if __name__ == "__main__":
    app.run(debug=True)
