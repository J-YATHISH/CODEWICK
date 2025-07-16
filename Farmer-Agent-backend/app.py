from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Add this line

from utils.internet import has_internet
from utils.audio_utils import transcribe_audio
from utils.image_utils import analyze_image_with_gemini
from utils.prompt_utils import build_prompt
from utils.ai_handler import get_ai_response
from utils.weather_utils import get_weather

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes and origins

@app.route("/farmer-agent", methods=["POST"])
def farmer_agent():
    try:
        text = request.form.get("text")
        city = request.form.get("city")
        lang = request.form.get("lang", "en")

        audio = request.files.get("audio")
        image = request.files.get("image")

        audio_text = transcribe_audio(audio) if audio else ""
        image_desc = analyze_image_with_gemini(image) if image else ""
        weather = get_weather(city or "")
        prompt = build_prompt(text, audio_text, image_desc, weather, lang)
        response = get_ai_response(prompt, has_internet(), lang)

        return jsonify({
            "city": city,
            "weather": weather,
            "ai_response": response,
            "input_used": {
                "text": text,
                "audio_text": audio_text,
                "image_description": image_desc
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
