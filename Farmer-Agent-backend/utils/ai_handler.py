import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_ai_response(prompt, online):
    if online:
        return call_openrouter(prompt)
    else:
        return call_ollama(prompt)  # You can keep this for offline fallback

def call_openrouter(prompt, model="mistralai/mistral-7b-instruct"):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a multilingual agricultural expert. Respond in Tamil."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        return response.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ OpenRouter error: {str(e)}"

def call_ollama(prompt):
    """
    Calls Ollama locally using gemma3:1b model.
    """
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "gemma3:1b",
            "prompt": prompt,
            "stream": False  # set to True if you want streamed responses
        })
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        return f"❌ Ollama (gemma3:1b) error: {str(e)}"
