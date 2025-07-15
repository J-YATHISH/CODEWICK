from flask import Blueprint, request, jsonify
from utils.weather_fetcher import get_weather
from utils.crop_logic import get_crop_advice, get_climate_tip

advisory_bp = Blueprint("advisory", __name__)

@advisory_bp.route("/", methods=["POST"])
def generate_advice():
    data = request.json
    crop = data.get("crop")
    city = data.get("city", "Coimbatore")

    weather = get_weather(city)
    if "error" in weather:
        return jsonify({"error": "Weather fetch failed"}), 500

    crop_advice = get_crop_advice(crop, weather)
    climate_tip = get_climate_tip(weather)

    return jsonify({
        "crop": crop,
        "city": city,
        "weather": weather,
        "advisory": crop_advice,
        "climate_tip": climate_tip
    })
