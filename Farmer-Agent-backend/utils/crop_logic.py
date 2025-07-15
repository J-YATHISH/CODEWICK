import json

with open("data/crop_advice.json") as f:
    CROP_DATA = json.load(f)

def get_crop_advice(crop, weather):
    data = CROP_DATA.get(crop.lower())
    if not data:
        return "No crop data found."

    advice = data["default_advice"]

    if "rain" in weather["condition"]:
        advice += " " + data["rain_warning"]

    if weather["temp"] > data["optimal_temp"][1]:
        advice += " " + data["heat_tip"]

    return advice

def get_climate_tip(weather):
    if weather["temp"] >= 35:
        return "⚠️ High heat! Use shade nets and reduce irrigation."
    elif "rain" in weather["condition"]:
        return "🌧️ Rain expected. Avoid fertilizer today."
    elif weather["humidity"] < 40:
        return "💧 Low humidity. Use drip irrigation or mulching."
    else:
        return "✅ Weather is favorable for most crops."
