from flask import Blueprint, request, jsonify
from utils.weather_fetcher import get_weather
from utils.crop_logic import get_crop_advice, get_climate_tip
from utils.gpt_engine import ask_gpt


advisory_bp = Blueprint("advisory", __name__)

@advisory_bp.route("/", methods=["POST"])
def generate_advice():
    data = request.json
    crop = data.get("crop")
    city = data.get("city", "Coimbatore")
    question = data.get("question", "How to grow this crop?")

    weather = get_weather(city)
    if "error" in weather:
        return jsonify({"error": "Weather fetch failed"}), 500

    crop_advice = get_crop_advice(crop, weather)
    climate_tip = get_climate_tip(weather)

    prompt = f"""
User Query: {question}
Crop: {crop}
City: {city}
Current Weather: {weather['temp']}°C, {weather['condition']}, humidity {weather['humidity']}%
Crop Advisory: {crop_advice}
Climate-Smart Tip: {climate_tip}
Respond like an agriculture expert in a simple and helpful tone. Use Tamil if appropriate.
"""

    ai_response = ask_gpt(prompt)

    return jsonify({
        "crop": crop,
        "city": city,
        "weather": weather,
        "advisory": crop_advice,
        "climate_tip": climate_tip,
        "ai_response": ai_response
    })

