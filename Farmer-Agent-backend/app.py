from flask import Flask, request, jsonify
from langdetect import detect
from utils.internet import has_internet
from utils.audio_utils import transcribe_audio
from utils.image_utils import analyze_image_with_gemini
from utils.prompt_utils import build_prompt
from utils.ai_handler import get_ai_response
from utils.weather_utils import get_weather

app = Flask(__name__)

# Helper function to detect supported languages
def detect_input_language(text, audio_text):
    combined = f"{text or ''} {audio_text or ''}".strip()
    try:
        lang_code = detect(combined)
        if lang_code in ["ta", "hi", "te", "ml"]:
            return lang_code
        else:
            return "en"
    except:
        return "en"

@app.route("/farmer-agent", methods=["POST"])
def farmer_agent():
    try:
        # 1. Get inputs from request
        text = request.form.get("text")
        city = request.form.get("city")
        audio = request.files.get("audio")
        image = request.files.get("image")

        # 2. Process audio and image (if present)
        audio_text = transcribe_audio(audio) if audio else ""
        image_desc = analyze_image_with_gemini(image) if image else ""

        # 3. Get weather
        weather = get_weather(city or "")

        # 4. Detect language
        lang = detect_input_language(text, audio_text)

        # 5. Build prompt
        prompt = build_prompt(text, audio_text, image_desc, weather, lang)

        # 6. Get AI response
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
