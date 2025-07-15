def build_prompt(text=None, audio_text="", image_desc="", weather=None, lang="ta"):
    text = text or ""
    audio_text = audio_text or ""
    image_desc = image_desc or ""
    weather = weather or {"temp": "NA", "humidity": "NA", "condition": "NA"}

    parts = []

    if text.strip():
        parts.append(f"📝 {text.strip()}")

    if audio_text.strip():
        parts.append(f"🎤 {audio_text.strip()}")

    if image_desc.strip():
        parts.append(f"🖼️ {image_desc.strip()}")

    input_summary = "\n".join(parts) or "[உள்ளீடு இல்லை / कोई इनपुट नहीं]"

    if lang == "hi":
        return f"""आप एक बुद्धिमान बहुभाषी कृषि सहायक AI हैं। किसान की जानकारी और मौसम के अनुसार हिंदी में सलाह दें।

{input_summary}

🌦️ मौसम की जानकारी:
- तापमान: {weather['temp']}°C
- स्थिति: {weather['condition']}
- नमी: {weather['humidity']}%

✅ कृपया:
1. हिंदी में सरल उत्तर दें।
2. वर्तमान मौसम के अनुसार कौन सी फसल बोनी चाहिए बताएं।
3. यदि ज़मीन या फसल में कोई समस्या हो तो सुझाव दें।
"""
    else:  # default: Tamil
        return f"""நீங்கள் ஒரு அறிவுள்ள பன்மொழி விவசாய ஆலோசகர் AI. 
விவசாயியின் உள்ளீடுகள் மற்றும் வானிலை அடிப்படையில் தமிழில் ஆலோசனை வழங்கவும்.

{input_summary}

🌦️ தற்போதைய வானிலை:
- வெப்பநிலை: {weather['temp']}°C
- நிலை: {weather['condition']}
- ஈரப்பதம்: {weather['humidity']}%

✅ உங்கள் பதிலில்:
1. தமிழில் எளிமையாக விளக்கவும்.
2. தற்போது என்ன விதைக்கலாம் என்பதைச் சொல்லவும்.
3. நிலம் அல்லது பயிர் தொடர்பான சிக்கல்கள் இருந்தால் பரிந்துரை செய்யவும்.
"""


'''def build_prompt(text=None, audio_text="", image_desc="", weather=None):
    """
    Builds a clear prompt combining all farmer inputs and weather.
    Returns a complete instruction string for the AI model.
    """
    text = text or ""
    audio_text = audio_text or ""
    image_desc = image_desc or ""
    weather = weather or {"temp": "NA", "humidity": "NA", "condition": "NA"}

    combined_input = " ".join([text.strip(), audio_text.strip(), image_desc.strip()]).strip()

    if not combined_input:
        combined_input = "[No input provided]"

    return f"""You are a multilingual agricultural assistant AI specialized in helping Tamil farmers.

Farmer's input (may include text, audio, or image description):
{combined_input}

Current weather in their area:
- 🌡 Temperature: {weather['temp']}°C
- 🌥 Condition: {weather['condition']}
- 💧 Humidity: {weather['humidity']}%

Please provide:
1. A useful and short farming recommendation (in Tamil).
2. If applicable, suggest what crop to plant now based on the input and weather.
3. Keep the response clear and beginner-friendly.
"""
'''