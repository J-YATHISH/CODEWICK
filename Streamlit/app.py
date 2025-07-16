import streamlit as st
import requests
import os
import tempfile
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
from deep_translator import GoogleTranslator

# ---------- CONFIG ----------
BACKEND_URL = "http://127.0.0.1:5000/farmer-agent"
LANGUAGES = {
    "English": "en",
    "Tamil (தமிழ்)": "ta",
    "Hindi (हिंदी)": "hi",
    "Telugu (తెలుగు)": "te",
    "Malayalam (മലയാളം)": "ml"
}
SAMPLE_RATE = 16000

# ---------- UI SETUP ----------
st.set_page_config(page_title="Agri Saarthi", layout="centered")
selected_lang = st.selectbox("🌐 Choose Language", list(LANGUAGES.keys()))
lang_code = LANGUAGES[selected_lang]

# ---------- Translation System (Fast, Cache + Clean) ----------
UI_STRINGS = [
    "Your AI Farming Assistant",
    "🎤 Record your voice question",
    "🎙️ Click to record your question",
    "Processing your voice...",
    "Your voice has been recorded successfully!",
    "📝 Or type your question below (optional)",
    "Type here...",
    "📸 Upload crop image (optional)",
    "Choose an image file",
    "🏙️ Enter your city or village name",
    "e.g., Salem",
    "🌾 Ask Agri Saarthi",
    "Please provide at least one input to get advice.",
    "🔍 Getting advice... Please wait",
    "🤖 AI Advice",
    "Spoken in",
    "Could not generate voice reply.",
    "Error while processing your request:",
    "Could not save audio:"
]

@st.cache_resource
def get_translation_map(lang_code):
    if lang_code == "en":
        return {text: text for text in UI_STRINGS}
    else:
        return {
            text: GoogleTranslator(source='en', target=lang_code).translate(text)
            for text in UI_STRINGS
        }

tmap = get_translation_map(lang_code)
def t(text): return tmap.get(text, text)

# ---------- HEADER ----------
st.markdown(f"""
<div style="background-color:#4CAF50;padding:20px;border-radius:10px;text-align:center;color:white;">
  <h1>🌿 Agri Saarthi</h1>
  <h4>{t("Your AI Farming Assistant")}</h4>
</div>
""", unsafe_allow_html=True)

# ---------- AUDIO RECORDING ----------
st.markdown(f"### {t('🎤 Record your voice question')}")
audio_bytes = audio_recorder(
    text=t("🎙️ Click to record your question"),
    sample_rate=SAMPLE_RATE
)

audio_path = None
if audio_bytes:
    with st.spinner(t("Processing your voice...")):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_bytes)
                audio_path = f.name
            st.audio(audio_path, format="audio/wav")
            st.success(t("Your voice has been recorded successfully!"))
        except Exception as e:
            st.error(t("Could not save audio:") + f" {e}")

# ---------- TEXT / IMAGE INPUT ----------
st.markdown(f"### {t('📝 Or type your question below (optional)')}")
text_input = st.text_area(t("Type here..."))

st.markdown(f"### {t('📸 Upload crop image (optional)')}")
image_file = st.file_uploader(t("Choose an image file"), type=["jpg", "jpeg"])

city = st.text_input(t("🏙️ Enter your city or village name"), placeholder=t("e.g., Salem"))

# ---------- SUBMIT ----------
if st.button(t("🌾 Ask Agri Saarthi")):
    if not (text_input or image_file or audio_path):
        st.warning(t("Please provide at least one input to get advice."))
    else:
        with st.spinner(t("🔍 Getting advice... Please wait")):
            try:
                data = {"text": text_input, "city": city, "lang": lang_code}
                files = {}

                if audio_path:
                    files["audio"] = (os.path.basename(audio_path), open(audio_path, "rb"), "audio/wav")
                if image_file:
                    files["image"] = (image_file.name, image_file, "image/jpeg")

                response = requests.post(BACKEND_URL, data=data, files=files, timeout=60)
                response.raise_for_status()

                result = response.json()
                ai_response = result.get("ai_response", "")

                st.markdown(f"### 🤖 {t('AI Advice')}")
                st.write(t(ai_response))

                # ---------- AI TTS Response ----------
                if ai_response:
                    try:
                        tts = gTTS(ai_response, lang=lang_code)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
                            tts_path = tf.name
                            tts.save(tts_path)

                        with open(tts_path, "rb") as f:
                            st.audio(f.read(), format="audio/mp3")
                            st.caption(f"🔊 {t('Spoken in')} {selected_lang}")

                        os.remove(tts_path)

                    except Exception as e:
                        st.warning(t("Could not generate voice reply.") + f" ({e})")

                # Clean up audio
                if audio_path and os.path.exists(audio_path):
                    try:
                        os.remove(audio_path)
                    except:
                        pass

            except Exception as e:
                st.error(t("Error while processing your request:") + f" {e}")

# import streamlit as st
# import requests
# import os
# import tempfile
# from audio_recorder_streamlit import audio_recorder
# from gtts import gTTS
# from deep_translator import GoogleTranslator

# # ---------- CONFIG ----------
# BACKEND_URL = "http://127.0.0.1:5000/farmer-agent"
# LANGUAGES = {
#     "English": "en",
#     "Tamil (தமிழ்)": "ta",
#     "Hindi (हिंदी)": "hi",
#     "Telugu (తెలుగు)": "te",
#     "Malayalam (മലയാളം)": "ml"
# }
# SAMPLE_RATE = 16000

# # ---------- UI SETUP ----------
# st.set_page_config(page_title="Agri Saarthi", layout="centered")

# selected_lang = st.selectbox("🌐 Choose Language", list(LANGUAGES.keys()))
# lang_code = LANGUAGES[selected_lang]

# def t(text):
#     if lang_code == "en":
#         return text
#     try:
#         return GoogleTranslator(source='en', target=lang_code).translate(text)
#     except:
#         return text

# st.markdown(f"""
# <div style="background-color:#4CAF50;padding:20px;border-radius:10px;text-align:center;color:white;">
#   <h1>🌿 Agri Saarthi</h1>
#   <h4>{t("Your AI Farming Assistant")}</h4>
# </div>
# """, unsafe_allow_html=True)

# # ---------- AUDIO RECORDING ----------
# st.markdown(f"### {t('🎤 Record your voice question')}")
# audio_bytes = audio_recorder(
#     text=t("🎙️ Click to record your question"),
#     sample_rate=SAMPLE_RATE
# )

# audio_path = None
# if audio_bytes:
#     with st.spinner(t("Processing your voice...")):
#         try:
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
#                 f.write(audio_bytes)
#                 audio_path = f.name
#             st.audio(audio_path, format="audio/wav")
#             st.success(t("Your voice has been recorded successfully!"))
#         except Exception as e:
#             st.error(t("Could not save audio: ") + str(e))

# # ---------- TEXT / IMAGE INPUT ----------
# st.markdown(f"### {t('📝 Or type your question below (optional)')}")
# text_input = st.text_area(t("Type here..."))

# st.markdown(f"### {t('📸 Upload crop image (optional)')}")
# image_file = st.file_uploader(t("Choose an image file"), type=["jpg", "jpeg"])

# city = st.text_input(t("🏙️ Enter your city or village name"), placeholder=t("e.g., Salem"))

# # ---------- SUBMIT ----------
# if st.button(t("🌾 Ask Agri Saarthi")):
#     if not (text_input or image_file or audio_path):
#         st.warning(t("Please provide at least one input to get advice."))
#     else:
#         with st.spinner(t("🔍 Getting advice... Please wait")):
#             try:
#                 data = {"text": text_input, "city": city, "lang": lang_code}
#                 files = {}

#                 if audio_path:
#                     files["audio"] = (os.path.basename(audio_path), open(audio_path, "rb"), "audio/wav")
#                 if image_file:
#                     files["image"] = (image_file.name, image_file, "image/jpeg")

#                 response = requests.post(BACKEND_URL, data=data, files=files, timeout=60)
#                 response.raise_for_status()

#                 result = response.json()
#                 ai_response = result.get("ai_response", "")

#                 st.markdown(f"### 🤖 {t('AI Advice')}")
#                 st.write(t(ai_response))

#                 # ---------- AI SPEECH (gTTS) ----------
#                 if ai_response:
#                     try:
#                         tts = gTTS(ai_response, lang=lang_code)
#                         with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
#                             tts_path = tf.name
#                             tts.save(tts_path)

#                         with open(tts_path, "rb") as f:
#                             st.audio(f.read(), format="audio/mp3")
#                             st.caption(f"🔊 {t('Spoken in')} {selected_lang}")

#                         os.remove(tts_path)

#                     except Exception as e:
#                         st.warning(t("Could not generate voice reply.") + f" ({e})")

#                 # Cleanup
#                 if audio_path and os.path.exists(audio_path):
#                     try:
#                         os.remove(audio_path)
#                     except:
#                         pass

#             except Exception as e:
#                 st.error(t("Error while processing your request: ") + str(e))