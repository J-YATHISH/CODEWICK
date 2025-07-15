import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {'category': f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "DANGEROUS_CONTENT"]
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

input_prompt = (
    "You are a helpful crop expert who speaks simply for rural farmers.\n"
    "This is a plant with... "
    "In very simple and short sentences, explain what this disease is, how it happens, "
    "and how a farmer can treat and stop it. Use easy words any farmer can understand."
)

def analyze_image_with_gemini(image_file):
    """
    image_file: werkzeug FileStorage object (from request.files.get("image"))
    """
    image_data = {
        "mime_type": image_file.mimetype,
        "data": image_file.read()  # read bytes directly from the in-memory object
    }

    response = model.generate_content([input_prompt, image_data])
    return response.text
