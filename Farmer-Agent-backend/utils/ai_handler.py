import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_openrouter(prompt, lang="ta", model="deepseek/deepseek-chat"):
    try:
        # System prompt based on language
        system_prompt = {
            "ta": "நீங்கள் ஒரு விவசாய ஆலோசகர். தமிழில் பதிலளிக்கவும்.",
            "hi": "आप एक कृषि सलाहकार हैं। कृपया हिंदी में उत्तर दें।",
            "te": "మీరు ఒక వ్యవసాయ సలహాదారు. దయచేసి తెలుగులో సమాధానం ఇవ్వండి.",
            "ml": "നിങ്ങൾ ഒരു കാർഷിക ഉപദേശകനാണ്. ദയവായി മലയാളത്തിൽ മറുപടി നൽകുക."
        }.get(lang, "You are a multilingual agricultural advisor AI.")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 512
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            return f"❌ OpenRouter HTTP error {response.status_code}: {response.text}"

        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"❌ OpenRouter error: {data['error']}"
        else:
            return f"❌ OpenRouter error: Unexpected response format: {data}"

    except Exception as e:
        return f"❌ OpenRouter exception: {str(e)}"

def call_ollama(prompt, lang="ta"):
    try:
        system_prompt = {
            "ta": "நீங்கள் ஒரு விவசாய ஆலோசகர். தமிழில் பதிலளிக்கவும்.",
            "hi": "आप एक कृषि सलाहकार हैं। कृपया हिंदी में उत्तर दें।",
            "te": "మీరు ఒక వ్యవసాయ సలహాదారు. దయచేసి తెలుగులో సమాధానం ఇవ్వండి.",
            "ml": "നിങ്ങൾ ഒരു കാർഷിക ഉപദേശകനാണ്. ദയവായി മലയാളത്തിൽ മറുപടി നൽകുക."
        }.get(lang, "You are a multilingual agricultural advisor AI.")

        full_prompt = f"{system_prompt}\n\n{prompt}"

        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "gemma:3b",
            "prompt": full_prompt,
            "stream": False
        })

        result = response.json()
        return result.get("response", "❌ Ollama: No response returned")

    except Exception as e:
        return f"❌ Ollama error: {str(e)}"

def get_ai_response(prompt, online, lang="ta"):
    if online:
        return call_openrouter(prompt, lang=lang)
    else:
        return call_ollama(prompt, lang=lang)
