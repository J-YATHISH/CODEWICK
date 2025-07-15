import requests

def ask_gpt(prompt):
    try:
        HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200}
        }

        headers = {
            "Content-Type": "application/json"
        }

        res = requests.post(HF_API_URL, json=payload, headers=headers)

        if res.status_code == 200:
            result = res.json()
            return result[0]['generated_text'] if isinstance(result, list) else result
        elif res.status_code == 503:
            return "⏳ Model is loading. Try again shortly."
        else:
            return f"❌ HuggingFace error: {res.status_code} - {res.text}"

    except Exception as e:
        return f"❌ Exception: {str(e)}"
