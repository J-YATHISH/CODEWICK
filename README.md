# 🌱 CODEWICK: AI-Powered Farming Assistant

**CODEWICK** is an AI-driven agricultural assistant that empowers farmers through image-based crop diagnosis, voice queries, localized weather-aware advice, and multilingual support — all in a single, intuitive platform.

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
CODEWICK/
├── README.md                     # Project documentation
├── nill.txt                      # Placeholder for commits
├── Streamlit/
│   └── app.py                    # Streamlit frontend (UI & voice/image upload)
└── Farmer-Agent-backend/
    ├── appnew.py                 # Gradio-based AI image advisory
    ├── test.py                   # Test for HuggingFace image captioning
    ├── routes/
    │   ├── advisory.py           # Crop advice route (weather + AI)
    │   └── weather.py            # Weather route
    └── utils/
        ├── audio_utils.py        # Audio transcription via AssemblyAI
        └── image_utils.py        # Image processing for AI models


🧠 Technologies Used

Frontend: Streamlit
Backend: Flask, Gradio
AI Models: Google Gemini, HuggingFace
Speech Processing: AssemblyAI (input), gTTS (output)
Weather API: OpenWeather or similar (customized)

🛠️ How to Run

1. Clone the Repo

git clone https://github.com/J-YATHISH/CODEWICK.git
cd CODEWICK

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
