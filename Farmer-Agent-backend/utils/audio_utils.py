import os
from dotenv import load_dotenv
import assemblyai as aai

load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_KEY")

def transcribe_audio(audio_file, lang="ta"):  # default is Tamil
    """
    Transcribes the uploaded audio file using AssemblyAI for the given language.
    Supported: "ta" (Tamil), "hi" (Hindi)
    """
    path = "static/temp_audio.wav"
    audio_file.save(path)

    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(
            path,
            config=aai.TranscriptionConfig(language_code=lang)
        )
        return transcript.text
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return ""