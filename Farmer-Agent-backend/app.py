from flask import Flask, request, jsonify
from utils.internet import has_internet
from utils.audio_utils import transcribe_audio
from utils.image_utils import describe_image
from utils.prompt_utils import build_prompt
from utils.ai_handler import get_ai_response
from utils.weather_utils import get_weather

app = Flask(__name__)

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
        image_desc = describe_image(image) if image else ""

        # 3. Get weather
        weather = get_weather(city or "")

        # 4. Build prompt
        prompt = build_prompt(text, audio_text, image_desc, weather)

        # 5. Get AI response (online/offline)
        response = get_ai_response(prompt, has_internet())

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
