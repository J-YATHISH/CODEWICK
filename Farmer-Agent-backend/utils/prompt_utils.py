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

    input_summary = "\n".join(parts) or "[No input]"

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
    elif lang == "en":
        return f"""You are a smart multilingual agricultural assistant AI. Based on the farmer's input and weather, reply in clear and simple English.

{input_summary}

🌦️ Current Weather:
- Temperature: {weather['temp']}°C
- Condition: {weather['condition']}
- Humidity: {weather['humidity']}%

✅ Please:
1. Respond in English simply.
2. Suggest what crop can be planted now.
3. Give advice if there is any field or crop issue.
"""
    elif lang == "te":
        return f"""మీరు తెలుగులో సమాధానాలు ఇచ్చే తెలివైన బహుభాషా వ్యవసాయ సహాయక AI. రైతు ఇచ్చిన సమాచారం మరియు వాతావరణాన్ని బట్టి తెలుగులో సలహా ఇవ్వండి.

{input_summary}

🌦️ వాతావరణ సమాచారం:
- ఉష్ణోగ్రత: {weather['temp']}°C
- పరిస్థితి: {weather['condition']}
- ఆర్ద్రత: {weather['humidity']}%

✅ దయచేసి:
1. సరళమైన తెలుగులో సమాధానం ఇవ్వండి.
2. ఇప్పుడు ఏ పంట వేయాలో సూచించండి.
3. భూమి లేదా పంట సమస్యలు ఉంటే సలహా ఇవ్వండి.
"""
    elif lang == "ml":
        return f"""നിങ്ങൾ മലയാളത്തിൽ ഉത്തരം നൽകുന്ന ബഹുഭാഷാ കാർഷിക സഹായ AI ആണു. കർഷകന്റെ വിവരങ്ങളും കാലാവസ്ഥയും അടിസ്ഥാനമാക്കി മലയാളത്തിൽ ഉപദേശം നൽകുക.

{input_summary}

🌦️ കാലാവസ്ഥാ വിവരങ്ങൾ:
- താപനില: {weather['temp']}°C
- അവസ്ഥ: {weather['condition']}
- ഈർപ്പം: {weather['humidity']}%

✅ ദയവായി:
1. ലളിതമായ മലയാളത്തിൽ മറുപടി നൽകുക.
2. ഇപ്പോൾ എത് വിളം വളർത്താമെന്നു നിർദേശിക്കുക.
3. മണ്ണോ വിളയിലോ പ്രശ്നങ്ങൾ ഉണ്ടെങ്കിൽ ഉപദേശം നൽകുക.
"""
    else:
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
