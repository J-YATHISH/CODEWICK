from flask import Blueprint, request, jsonify
from utils.weather_fetcher import get_weather

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/", methods=["GET"])
def weather():
    city = request.args.get("city", "Coimbatore")
    weather_data = get_weather(city)
    return jsonify(weather_data)
