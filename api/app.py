from flask import Flask, request, jsonify 
from flask_cors import CORS
import random, json
from deep_translator import GoogleTranslator
import requests

app = Flask(__name__)
CORS(app)

# Try reading places.json with fallback encoding
try:
    with open("places.json", "r", encoding="utf-8") as f:
        places_data = json.load(f)
except UnicodeDecodeError:
    with open("places.json", "r", encoding="latin-1") as f:
        places_data = json.load(f)

# Basic conversation responses
basic_responses = {
    "hi": "Hello! How can I help you today? Just write the name of the city you want info about..",
    "hello": "Hi there! Ready to explore? Just write the name of the city you want info about..",
    "hey": "Hey! How’s it going? Just write the name of the city you want info about..",
    "i am good": "Nice to listen that",
    "good morning": "Good morning! Have a great day ahead 🌞",
    "good afternoon": "Good afternoon! What city are you curious about?",
    "good evening": "Good evening! How can I assist you?",
    "how are you": "I'm doing great, thanks for asking! How about you?",
    "what is your name": "I am KANHA, your travel companion chatbot!",
    "tell your name": "My name is KANHA 😊",
    "who made you": "I was created by you, with Python, Flask, and a lot of love ❤️",
    "what do you do": "I help you explore cities, show weather reports, and answer questions!",
    "tell me a joke": random.choice([
        "Why don’t skeletons ever fight each other? Because they don’t have the guts!",
        "I told my computer I needed a break, and it said 'No problem — I’ll go to sleep.' 😂",
        "Why was the math book sad? Because it had too many problems."
    ]),
    "thank you": "You're welcome! 😊",
    "thanks": "Happy to help!",
    "bye": "Goodbye! Have a safe journey ✈️",
    "goodbye": "See you soon! Take care 👋"
}

# OpenWeatherMap API Key
OPENWEATHER_API_KEY = "5ca369a1da6d22f78e6f3cb1a0899b58"

def get_weather_report(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    try:
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()
        if data.get("cod") != 200:
            return None, None
        # Extract weather info
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        weather_html = (
            f"<tr><th colspan='2'>Weather Report</th></tr>"
            f"<tr><td>Description</td><td>{weather_desc}</td></tr>"
            f"<tr><td>Temperature</td><td>{temp} °C</td></tr>"
            f"<tr><td>Humidity</td><td>{humidity}%</td></tr>"
            f"<tr><td>Wind Speed</td><td>{wind} m/s</td></tr>"
        )
        return weather_html, data
    except Exception as e:
        print("Weather API error:", e)
        return None, None

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input_raw = data.get("message", "").strip()
    user_input = user_input_raw.lower()
    print("User input (cleaned):", user_input)
    print("Available cities:", list(places_data.keys()))

    language = data.get("language", "en-US")
    gender = data.get("gender", "female")

    reply_html = ""
    plain_reply = ""

    # 1. Basic responses
    for key, resp in basic_responses.items():
        if key in user_input:
            reply_html = resp
            plain_reply = resp
            break

    # 2. City / Weather
    if reply_html == "":
        weather_html, weather_data = get_weather_report(user_input_raw)
        city_info = places_data.get(user_input)

        if weather_html or city_info:
            table = "<table class='info-table'>"
            table += f"<tr><th>City</th><td>{user_input_raw.title()}</td></tr>"

            if city_info:
                for k, v in city_info.items():
                    table += f"<tr><th>{k.title().replace('_',' ')}</th><td>{v}</td></tr>"

            if weather_html:
                table += weather_html
                plain_weather = (
                    f"Weather in {user_input_raw.title()}: "
                    f"{weather_data['weather'][0]['description'].capitalize()}, "
                    f"{weather_data['main']['temp']}°C, "
                    f"Humidity {weather_data['main']['humidity']}%, "
                    f"Wind {weather_data['wind']['speed']} m/s"
                )
            else:
                table += "<tr><td colspan='2'>Weather data not available.</td></tr>"
                plain_weather = "Weather data not available."

            table += "</table>"

            reply_html = table
            plain_reply = f"{user_input_raw.title()} info: " + ", ".join(f"{k}: {v}" for k, v in city_info.items()) if city_info else ""
            if weather_data:
                plain_reply += "; " + plain_weather
        else:
            reply_html = "Hey! I appreciate your patience, can you just provide me the city name you are curious to know about, thanks for coorporation."
            plain_reply = reply_html

    # 3. Translate
    if language != "en-US":
        try:
            translated = GoogleTranslator(source="auto", target=language.split('-')[0]).translate(plain_reply)
            reply_html = translated
            plain_reply = translated
        except Exception as e:
            print("Translation failed:", e)

    return jsonify({
        "reply": reply_html,
        "plain_reply": plain_reply,
        "language": language,
        "gender": gender
    })

# ✅ Vercel handler
from mangum import Mangum
handler = Mangum(app)

# ✅ Local run
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
