# 🌱 AGRI SAARTHI - Revolutionizing Agriculture with AI

**AGRI SAARTHI** is an AI-driven agricultural assistant that empowers farmers through image-based crop diagnosis, voice queries, localized weather-aware advice, and multilingual support — all in a single, intuitive platform.

---

## 🚀 Key Features

- 🎤 **Voice & Text Queries** — Ask farming questions using voice or text in multiple Indian languages.
- 📸 **Image Diagnosis** — Upload crop images to detect plant diseases using Google Gemini and HuggingFace.
- 🌦️ **Weather-Aware Tips** — Input your village/city to get personalized, climate-sensitive farming advice.
- 🗣️ **Multilingual Support** — English, Tamil, Hindi, Telugu, Malayalam.
- 🔊 **Voice Output** — Replies are spoken back to the user using gTTS for accessibility.

---

## 🏗️ Project Structure

```bash
D:\CODEWICK-AgriSaarthi
│   .gitignore
│   README.md
│   styles.css
│
├───Farmer-Agent-backend
│   │   .env
│   │   app.py
│   │   requirements.txt
│   │   test.py
│   │
│   ├───routes
│   │   │   advisory.py
│   │   │   weather.py
│   │   │
│   │   └───_pycache_
│   │           advisory.cpython-312.pyc
│   │           weather.cpython-312.pyc
│   │
│   ├───static
│   │       temp_audio.wav
│   │       temp_image.jpg
│   │
│   └───utils
│       │   ai_handler.py
│       │   audio_utils.py
│       │   image_utils.py
│       │   internet.py
│       │   prompt_utils.py
│       │   weather_utils.py
│       │
│       └───_pycache_
│               ai_handler.cpython-312.pyc
│               audio_utils.cpython-312.pyc
│               crop_logic.cpython-312.pyc
│               gpt_engine.cpython-312.pyc
│               image_utils.cpython-312.pyc
│               internet.cpython-312.pyc
│               prompt_utils.cpython-312.pyc
│               weather_fetcher.cpython-312.pyc
│               weather_utils.cpython-312.pyc
│
├───offline
│       chatbot1.ipynb
│       farming_threats.pdf
│       rag.py
│
└───Streamlit
        app.py
        requirements.txt
        tts_23029baa098e48aba1d0db501cd23e9e.mp3


🧠 Technologies Used

Frontend: Streamlit
Backend: Flask, Gradio
AI Models: Google Gemini, HuggingFace
Speech Processing: AssemblyAI (input), gTTS (output)
Weather API: OpenWeather or similar (customized)

🛠️ How to Run

1. Clone the Repo

git clone https://github.com/J-YATHISH/CODEWICK-AgriSaarthi
cd CODEWICK-AgriSaarthi

2. Set Environment Variables

Create a .env file in the root folder and add:

GOOGLE_API_KEY=your_google_api_key
ASSEMBLYAI_API_KEY=your_assembly_ai_key
HUGGINGFACE_API_KEY=your_huggingface_token
OPENWEATHER_API = your_openweatherapi
OPENROUTER_API=your_openrouter_api

3. Install Requirements

You may need to install requirements for both frontend and backend parts. Example:

pip install streamlit flask gradio openai google-generativeai gtts requests

4. Run Backend

cd Farmer-Agent-backend
python appnew.py

5. Run Frontend


cd ../Streamlit
streamlit run app.py
