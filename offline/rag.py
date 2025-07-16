import os
import streamlit as st
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from googletrans import Translator

# Custom CSS Styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize models
@st.cache_resource
def setup_models():
    # RAG System
    loader = PyPDFLoader('farming_threats.pdf')
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma.from_documents(documents, embeddings)
    llm = Ollama(model="gemma3:1b", temperature=0.7)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())
    
    # Disease Detection Model
    disease_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor()
    ])
    
    return qa_chain, disease_model, transform

# Translation function
def translate_text(text, dest_lang):
    lang_map = {
        "English": "en",
        "Tamil": "ta",
        "Hindi": "hi",
        "Telugu": "te"
    }
    try:
        translator = Translator()
        translated = translator.translate(text, dest=lang_map[dest_lang])
        return translated.text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text

# Voice transcription
def transcribe_audio(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as fp:
            fp.write(audio_bytes)
            audio_path = fp.name
        
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)


        try:
            text = r.recognize_google(audio, language="ta-IN")
            return text, "Tamil"
        except:
            text = r.recognize_google(audio, language="en-IN")
            return text, "English"
    except Exception as e:
        st.error(f"Audio processing error: {str(e)}")
        return None, "English"

# Disease detection
def detect_disease(image, model, transform):
    img = Image.open(image).convert('RGB')
    img_t = transform(img).unsqueeze(0)
    results = model(img_t)
    predictions = results.pandas().xyxy[0]
    return predictions['name'][0] if len(predictions) > 0 else "Healthy"

# Main App
def main():
    st.set_page_config(page_title="AgriSaarthi", layout="wide", page_icon="🌿")
    local_css("styles.css")
    
    # Header
    st.markdown("""
    <div class="header">
        <h1>🌿 AgriSaarthi</h1>
        <p>Your Intelligent Farming Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize models
    qa_chain, disease_model, transform = setup_models()
    
    # User selection
    col1, col2 = st.columns(2)
    with col1:
        user_type = st.radio("You are:", ["Farmer 👨‍🌾", "Gardener 🌱"], horizontal=True)
    with col2:
        language = st.selectbox("Response Language:", 
                              ["English", "Tamil", "Hindi", "Telugu"])
    
    # Input methods
    st.markdown("### Ask Your Question")
    input_method = st.radio("", 
                          ["Text ✍️", "Voice 🎤", "Image 📷"], 
                          horizontal=True,
                          label_visibility="collapsed")
    
    question = None
    detected_lang = "English"
    
    if input_method == "Text ✍️":
        question = st.text_area("Type your question:", height=100)
    elif input_method == "Voice 🎤":
        audio_bytes = audio_recorder(pause_threshold=2.0)
        if audio_bytes:
            with st.spinner("Processing your voice..."):
                question, detected_lang = transcribe_audio(audio_bytes)
                if question:
                    st.text_area("Your question:", value=question, height=100)
    else:
        uploaded_file = st.file_uploader("Upload plant image:", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="Your Plant", use_column_width=True)
            if st.button("Analyze Plant"):
                with st.spinner("Diagnosing..."):
                    disease = detect_disease(uploaded_file, disease_model, transform)
                    st.success(f"Diagnosis: {disease}")
    
    # Get Answer
    if question and st.button("Get Answer", type="primary"):
        with st.spinner("Generating answer..."):
            try:
                # Get response
                response = qa_chain.invoke({"query": question})['result']
                
                # Translate if needed
                display_lang = detected_lang if detected_lang != "English" else language
                if display_lang != "English":
                    response = translate_text(response, display_lang)
                
                # Display answer
                st.markdown(f"""
                <div class="response-box">
                    <h3>💡 Answer ({display_lang})</h3>
                    <p>{response}</p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main()
'''import os
import streamlit as st
from PIL import Image
import numpy as np
import torch
from torchvision import transforms
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from translate import Translator

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize all models
@st.cache_resource
def setup_models():
    # 1. Setup RAG system
    loader = PyPDFLoader('farming_threats.pdf')
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma.from_documents(documents[:20], embeddings)
    
    # 2. Setup disease detection (example with YOLOv5)
    disease_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Replace with your model
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor()
    ])
    
    return db, disease_model, transform

# Translation function with caching
@st.cache_data
def translate_text(text, target_lang):
    lang_map = {
        "English": "en",
        "Tamil": "ta",
        "Hindi": "hi",
        "Telugu": "te",
        "Kannada": "kn",
        "Malayalam": "ml"
    }
    
    if target_lang == "English":
        return text
        
    try:
        translator = Translator(to_lang=lang_map[target_lang])
        translated = translator.translate(text)
        return translated
    except Exception as e:
        st.error(f"Translation failed: {str(e)}")
        return text

# Voice transcription with language detection
def transcribe_audio(audio_bytes):
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, "audio.wav")
        
        # Save audio bytes to file
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)
            
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
            
        try:
            # First try Tamil
            text = r.recognize_google(audio, language="ta-IN")
            detected_lang = "Tamil"
        except:
            # Fallback to English
            text = r.recognize_google(audio, language="en-IN")
            detected_lang = "English"
            
        # Clean up
        os.remove(audio_path)
        os.rmdir(temp_dir)
        
        return text, detected_lang
        
    except Exception as e:
        st.error(f"Voice recognition error: {str(e)}")
        return None, "English"

# Disease detection
def detect_disease(image, model, transform):
    img = Image.open(image).convert('RGB')
    img_t = transform(img).unsqueeze(0)
    results = model(img_t)
    predictions = results.pandas().xyxy[0]
    return predictions['name'][0] if len(predictions) > 0 else "Healthy"

# Streamlit UI
st.set_page_config(page_title="AgriSaarthi", layout="wide", page_icon="🌿")
local_css("styles.css")

# Custom header
st.markdown("""
<div class="header">
    <h1 style="color: white;">🌿 AgriSaarthi - Your Farming Companion</h1>
</div>
""", unsafe_allow_html=True)

# User type selection
st.markdown("### Select your mode:")
col1, col2 = st.columns(2)
with col1:
    if st.button("Farmer 👨‍🌾 (Professional)", use_container_width=True, key="farmer_btn"):
        st.session_state.user_type = "Farmer"
with col2:
    if st.button("Gardener 🌱 (Home)", use_container_width=True, key="gardener_btn"):
        st.session_state.user_type = "Gardener"

user_type = st.session_state.get("user_type", "Farmer")

# Language selection
language = st.selectbox("Choose response language:", 
                       ["English", "Tamil", "Hindi", "Telugu", "Kannada", "Malayalam"])

# Initialize models
db, disease_model, transform = setup_models()

# Customize responses based on user type
expertise = "professional large-scale" if user_type == "Farmer" else "home gardening"
system_prompt = f"""You're a {expertise} expert. Give {expertise} advice with {"technical details" if user_type == "Farmer" else "simple steps"}."""

# Create LangChain
llm = Ollama(model="gemma3:1b", temperature=0.7)
prompt = ChatPromptTemplate.from_template(f"""
{system_prompt}
Context: {{context}}
Question: {{input}}""")
chain = create_retrieval_chain(
    db.as_retriever(),
    create_stuff_documents_chain(llm, prompt)
)

# Input options
input_method = st.radio("Choose input method:", 
                       ["Text ✍️", "Voice 🎤", "Image 📷"], 
                       horizontal=True,
                       label_visibility="collapsed")

# Text/Voice input
if input_method != "Image 📷":
    if input_method == "Voice 🎤":
        st.markdown("### Speak your question:")
        audio_bytes = audio_recorder(
            pause_threshold=2.0,
            icon_size="2x",
            text="Press to record",
            energy_threshold=(-20.0, 20.0),
            sample_rate=44100,
        )
        
        if audio_bytes and len(audio_bytes) > 0:
            with st.spinner("Processing your voice..."):
                question, detected_lang = transcribe_audio(audio_bytes)
                if question:
                    st.session_state.voice_question = question
                    if detected_lang != "English":
                        st.session_state.language = detected_lang
                
            if 'voice_question' in st.session_state:
                st.text_input("Your question:", 
                             value=st.session_state.voice_question, 
                             key="voice_question_display")
    else:
        question = st.text_input("Your question:", 
                               placeholder="Type your farming question here...",
                               key="text_question")

    if st.button("Get Answer", type="primary") and 'question' in locals():
        with st.spinner("Researching..."):
            response = chain.invoke({"input": question})
            translated_answer = translate_text(response['answer'], language)
            
            st.markdown(f"""
            <div class="response-box">
                <h3>💡 Answer ({language})</h3>
                <p>{translated_answer}</p>
            </div>
            """, unsafe_allow_html=True)

# Image input
else:
    uploaded_file = st.file_uploader("Upload plant photo:", 
                                    type=["jpg", "png", "jpeg"],
                                    accept_multiple_files=False)
    if uploaded_file:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Your plant", use_column_width=True)
        
        with st.spinner("Diagnosing..."):
            disease = detect_disease(uploaded_file, disease_model, transform)
            
            if disease == "Healthy":
                st.markdown("""
                <div class="healthy-box">
                    <h3>🔍 Diagnosis</h3>
                    <p>✅ Healthy Plant</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="disease-box">
                    <h3>🔍 Diagnosis</h3>
                    <p>⚠️ {disease}</p>
                </div>
                """, unsafe_allow_html=True)
                
                treatment = chain.invoke({"input": f"{expertise} treatment for {disease}?"})
                translated_treatment = translate_text(treatment['answer'], language)
                
                st.markdown(f"""
                <div class="treatment-box">
                    <h3>💊 Treatment ({language})</h3>
                    <p>{translated_treatment}</p>
                </div>
                """, unsafe_allow_html=True)

# Instructions expander
with st.expander("ℹ️ How to use AgriSaarthi", expanded=False):
    st.markdown("""
    <div class="instructions">
        <h4>Getting Started</h4>
        <ul>
            <li><strong>Farmers</strong>: Get technical advice for large-scale operations</li>
            <li><strong>Gardeners</strong>: Receive simple home gardening tips</li>
            <li><strong>Multilingual Support</strong>: Ask questions in your preferred language</li>
        </ul>
        
        <h4>Input Methods</h4>
        <ul>
            <li><strong>Voice</strong>: Press mic, speak clearly, release to submit</li>
            <li><strong>Images</strong>: Upload clear photos of affected plants</li>
            <li><strong>Text</strong>: Type your questions directly</li>
        </ul>
        
        <h4>Supported Languages</h4>
        <div class="language-tags">
            <span class="tag">English</span>
            <span class="tag">தமிழ்</span>
            <span class="tag">हिन्दी</span>
            <span class="tag">తెలుగు</span>
            <span class="tag">ಕನ್ನಡ</span>
            <span class="tag">മലയാളം</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🌱 AgriSaarthi - Empowering Farmers and Gardeners with AI</p>
</div>
""", unsafe_allow_html=True)
'''

'''import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import tempfile
import speech_recognition as sr
from audio_recorder_streamlit import audio_recorder

# App config
st.set_page_config(page_title="🌱 AgriVoice Bot", layout="wide")
st.title("🌱 AgriVoice Bot")

# Initialize components
@st.cache_resource
def setup_chain():
    loader = PyPDFLoader('farming_threats.pdf')
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma.from_documents(documents[:20], embeddings)
    return db

# User type selection
user_type = st.radio(
    "Select your profile:",
    ("Farmer 👨‍🌾", "Gardener 🌿"),
    horizontal=True,
    key="user_type"
)

# Custom prompts
if "Farmer" in user_type:
    system_prompt = """You're an expert farming assistant. Provide detailed, 
    practical advice for large-scale agriculture using professional terminology."""
else:
    system_prompt = """You're a friendly gardening assistant. Give simple, 
    actionable tips using easy-to-understand language."""

# Initialize chain
db = setup_chain()
llm = Ollama(model="gemma3:1b", temperature=0.7)

prompt = ChatPromptTemplate.from_template(f"""
{system_prompt}
Context:
{{context}}
Question: {{input}}""")

chain = create_retrieval_chain(
    db.as_retriever(),
    create_stuff_documents_chain(llm, prompt)
)

# Voice input handler
def transcribe_audio(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as fp:
            fp.write(audio_bytes)
            r = sr.Recognizer()
            with sr.AudioFile(fp.name) as source:
                audio = r.record(source)
            return r.recognize_google(audio)
    except Exception as e:
        st.error(f"Voice recognition error: {str(e)}")
        return None

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input options
input_col, voice_col = st.columns([4, 1])
with input_col:
    text_input = st.chat_input("Type your question...")
with voice_col:
    audio_bytes = audio_recorder(pause_threshold=2.0)

# Process voice input
if audio_bytes and len(audio_bytes) > 0:
    text_input = transcribe_audio(audio_bytes)
    if text_input:
        st.session_state.messages.append({"role": "user", "content": f"🎤: {text_input}"})
        with st.chat_message("user"):
            st.markdown(f"🎤: {text_input}")

# Process text input
if text_input:
    if not audio_bytes or len(audio_bytes) == 0:  # Don't duplicate if voice input
        st.session_state.messages.append({"role": "user", "content": text_input})
        with st.chat_message("user"):
            st.markdown(text_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chain.invoke({"input": text_input})
            answer = response['answer']
            
            # Format response with emojis
            formatted_answer = answer.replace("Solution:", "🛠️ Solution:")\
                                    .replace("Tip:", "💡 Tip:")\
                                    .replace("Warning:", "⚠️ Warning:")
            
            st.markdown(formatted_answer)
            st.session_state.messages.append({"role": "assistant", "content": formatted_answer})

'''
'''
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# App config
st.set_page_config(page_title="AgriSaarthi",layout="wide")
st.title("🌱 AgriSaarthi Assistant")

# Initialize components (cached)
@st.cache_resource
def setup_chain():
    # Load PDF
    loader = PyPDFLoader('farming_threats.pdf')
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = text_splitter.split_documents(docs)
    
    # Vector store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma.from_documents(documents[:20], embeddings)
    
    return db

# User type selection
user_type = st.radio(
    "Select your profile:",
    ("Farmer 👨‍🌾", "Gardener 🌿"),
    horizontal=True
)

# Customize prompt based on user type
if "Farmer" in user_type:
    system_prompt = """You're an expert farming assistant. Provide detailed, 
    practical advice for large-scale agriculture. Focus on crop yields, 
    pest control, and modern farming techniques."""
else:
    system_prompt = """You're a friendly gardening assistant. Give simple, 
    actionable tips for home gardens. Focus on small spaces, organic 
    solutions, and beginner-friendly advice."""

# Initialize chain with custom prompt
db = setup_chain()
llm = Ollama(model="gemma3:1b", temperature=0.7)

prompt = ChatPromptTemplate.from_template(f"""
{system_prompt}
Answer based on this context:
<context>
{{context}}
</context>
Question: {{input}}""")

document_chain = create_stuff_documents_chain(llm, prompt)
retriever = db.as_retriever()
chain = create_retrieval_chain(retriever, document_chain)

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chain.invoke({"input": prompt})
            answer = response['answer']
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        '''
