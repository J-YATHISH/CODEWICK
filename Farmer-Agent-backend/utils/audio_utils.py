import os
from dotenv import load_dotenv
import assemblyai as aai

# Load API key from .env file
load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_KEY")  # Ensure .env contains ASSEMBLYAI_KEY

def transcribe_audio(audio_file):
    """
    Saves the uploaded audio file, transcribes it using AssemblyAI,
    and returns the English transcript.
    """

    # Save the uploaded file to disk temporarily
    path = "static/temp_audio.wav"
    audio_file.save(path)

    # Create a transcriber instance
    transcriber = aai.Transcriber()

    # Transcribe the audio with optional translation
    try:
        transcript = transcriber.transcribe(
            path,
            config=aai.TranscriptionConfig(
                # Auto-detect input language and translate to English
                translate_to="en"
            )
        )
        return transcript.text

    except Exception as e:
        return f"❌ Transcription failed: {str(e)}"
