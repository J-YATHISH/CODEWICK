def build_prompt(text=None, audio_text="", image_desc="", weather=None):
    """
    Builds a prompt combining text, transcribed audio, image description, and weather.
    Returns a complete prompt to send to an AI model.
    """
    text = text or ""
    audio_text = audio_text or ""
    image_desc = image_desc or ""
    weather = weather or {"temp": "NA", "humidity": "NA", "condition": "NA"}

    combined_input = " ".join([text.strip(), audio_text.strip(), image_desc.strip()]).strip()

    return f"""You are a multilingual agricultural advisor AI.

Input from farmer:
{combined_input or '[No input provided]'}

Current weather in location:
- Temperature: {weather['temp']}°C
- Condition: {weather['condition']}
- Humidity: {weather['humidity']}%

Provide a helpful advisory message and climate-smart suggestion in simple terms.
"""
